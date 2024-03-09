
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix
import copy
import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, numpy_full_list_cycle, changable_sockets, get_other_socket
from sverchok.utils.field.scalar import SvScalarField
from sverchok.utils.field.vector import SvVectorField
from sverchok.utils.sv_logging import sv_logger
from sverchok.utils.modules.matrix_utils import matrix_apply_np
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

import numpy as np
from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import calc_normals

transformation_dict = {
'SvVerticesSocket': 'VECTOR',
'SvMatrixSocket': 'MATRIX',
'SvStringsSocket': 'NUMBER',
'SvVectorFieldSocket': 'VECTOR_FIELD',
'SvScalarFieldSocket': 'SCALAR_FIELD'
}
def transform_mode(transformation):
    if isinstance(transformation[0], Matrix):
        transformation_mode = 'MATRIX'
    elif isinstance(transformation[0], SvScalarField):
        transformation_mode = 'SCALAR_FIELD'
    elif isinstance(transformation[0], SvVectorField):
        transformation_mode = 'VECTOR_FIELD'
    elif isinstance(transformation[0], np.ndarray):
        if transformation[0].shape[1] == 3:
            transformation_mode = 'VECTOR'
        else:
            transformation_mode = 'NUMBER'
    elif isinstance(transformation[0], (list, tuple)):
        if isinstance(transformation[0][0], (list, tuple)) and len(transformation[0][0]) == 3:
            transformation_mode = 'VECTOR'
        else:
            transformation_mode = 'NUMBER'
    else:
        raise Exception('Not Valid Transformation')

    return transformation_mode

def vector_transform(af_verts, transformation, transformation_mode, iterations, coeff):
    if transformation_mode == 'MATRIX':
        matrix = transformation
        for i in range(iterations):
            af_verts += (matrix_apply_np(af_verts, matrix)-af_verts)*coeff[i%len(coeff)]
    elif transformation_mode == 'VECTOR':
        offset_verts = numpy_full_list_cycle(np.array(transformation), af_verts.shape[0])
        for i in range(iterations):
            af_verts += offset_verts * coeff[i%len(coeff)]
    elif transformation_mode == 'VECTOR_FIELD':
        for i in range(iterations):
            i_coeff = coeff[i%len(coeff)]
            xs, ys, zs = transformation.evaluate_grid(af_verts[:, 0], af_verts[:, 1], af_verts[:, 2])
            af_verts[:, 0] += xs * i_coeff
            af_verts[:, 1] += ys * i_coeff
            af_verts[:, 2] += zs * i_coeff

    return af_verts


def number_transform(tris, transformation, verts, np_mask, use_mask, iterations, coeff):
    if len(transformation) == len(verts) and use_mask:
        offset_vals = (np.array(transformation)[np_mask])[:, np.newaxis]
    else:
        if use_mask:
            offset_vals = numpy_full_list_cycle(np.array(transformation), verts[np_mask].shape[0])[:, np.newaxis]
        else:
            offset_vals = numpy_full_list_cycle(np.array(transformation), verts.shape[0])[:, np.newaxis]


    for i in range(iterations):
        _, v_normals = calc_normals([verts, tris], v_normals=True, output_numpy=True, as_array=True)
        if use_mask:
            verts[np_mask] += v_normals[np_mask] * offset_vals * coeff[i%len(coeff)]
        else:
            verts += v_normals * offset_vals * coeff[i%len(coeff)]
    return verts

def scalar_field_transform(tris, transformation, verts, np_mask, use_mask, iterations, coeff):
    for i in range(iterations):
        _, v_normals = calc_normals([verts, tris], v_normals=True, output_numpy=True, as_array=True)
        if use_mask:
            offset_vals = transformation.evaluate_grid(verts[np_mask, 0], verts[np_mask, 1], verts[np_mask, 2])
            verts[np_mask] += v_normals[np_mask] * offset_vals[:, np.newaxis] * coeff[i%len(coeff)]
        else:
            offset_vals = transformation.evaluate_grid(verts[:, 0], verts[:, 1], verts[:, 2])
            verts += v_normals * offset_vals[:, np.newaxis] * coeff[i%len(coeff)]
    return verts

class SvO3Transform(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
    """
    Triggers: Open 3D Geometry Transform
    Tooltip: Apply Matrixes, Vector Fields and Scalar Fields to Open 3d Geometry
    """
    bl_idname = 'SvO3Transform'
    bl_label = 'Open3d Transform'
    bl_icon = 'MESH_DATA'
    sv_icon = 'SV_O3_OPEN3D_LOGO'
    sv_dependencies = ['open3d']
    
    methods = [
        ('VECTOR', "VECTOR", "", 0),
        ('MATRIX', "MATRIX", "", 1),
        ('NUMBER', "NUMBER", "", 2),
        ('VECTOR_FIELD', "VECTOR_FIELD", "", 3),
        ('SCALAR_FIELD', "SCALAR_FIELD", "", 4),
    ]

    method: EnumProperty(
        name="Method",
        items=methods,
        default='MATRIX')
    iterations: IntProperty(
        name="Iterations",
        default=1,
        update=updateNode)
    coefficient: FloatProperty(
        name="Coefficient",
        default=1,
        update=updateNode)

    def sv_init(self, context):
        self.width = 200
        geom = self.inputs.new('SvStringsSocket', "O3D Geometry")
        geom.is_mandatory = True
        geom.nesting_level = 1
        transf = self.inputs.new('SvStringsSocket', "Transformation")
        transf.is_mandatory = True
        transf.nesting_level = 1
        mask = self.inputs.new('SvStringsSocket', "Mask")
        mask.nesting_level = 2
        iterations = self.inputs.new('SvStringsSocket', "Iterations")
        iterations.prop_name = 'iterations'
        iterations.nesting_level = 1
        iterations.default_mode = 'EMPTY_LIST'
        iterations.pre_processing = 'ONE_ITEM'
        coeff = self.inputs.new('SvStringsSocket', "Coefficient")
        coeff.prop_name = 'coefficient'
        coeff.nesting_level = 2

        self.outputs.new('SvStringsSocket', "O3D Geometry")

    def sv_update(self):
        '''adapt socket type to input type'''
        if 'O3D Geometry' in self.inputs and self.inputs['O3D Geometry'].links:
            inputsocketname = 'O3D Geometry'
            outputsocketname = ['O3D Geometry']
            changable_sockets(self, inputsocketname, outputsocketname)
            if self.outputs['O3D Geometry'].bl_idname == 'SvO3TriangleMeshSocket':
                self.outputs['O3D Geometry'].label = 'O3D Triangle Mesh'
            else:
                self.outputs['O3D Geometry'].label = 'O3D Point Cloud'
            in_socket = self.inputs['Transformation']
            if in_socket.is_linked:
                in_other = get_other_socket(in_socket)
                if in_other:
                    s_type = in_other.bl_idname
                    self.method = transformation_dict[s_type]
    def pre_setup(self):
        if self.method == 'NUMBER':
            self.inputs['Transformation'].nesting_level = 2
        elif self.method == 'VECTOR':
            self.inputs['Transformation'].nesting_level = 3
        else:
            self.inputs['Transformation'].nesting_level = 1

    def process_data(self, params):
        mesh_out = []
        transformation_mode = self.method
        geometry_type = type(params[0][0])

        if geometry_type == o3d.cpu.pybind.geometry.TriangleMesh:
            geo_type = 'TRIS'
        elif geometry_type == o3d.cpu.pybind.geometry.PointCloud:
            geo_type = 'POINT_CLOUD'

        for mesh, transformation, mask, iterations, coeff in zip(*params):
            new_mesh = copy.deepcopy(mesh)
            use_mask = len(mask) > 0
            if geo_type == 'TRIS':
                verts = np.asarray(new_mesh.vertices)
            else:
                verts = np.asarray(new_mesh.points)
            if use_mask:
                np_mask = numpy_full_list_cycle(np.array(mask).astype('bool'), len(verts))
                af_verts = verts[np_mask]
            else:
                np_mask = []
                af_verts = verts
            if transformation_mode in ['MATRIX', 'VECTOR', 'VECTOR_FIELD']:
                af_verts = vector_transform(af_verts, transformation, transformation_mode, iterations, coeff)
                if use_mask:
                    verts[np_mask] = af_verts
                else:
                    verts = af_verts

            else:
                if geo_type == 'TRIS':
                    tris = np.asarray(mesh.triangles)
                    if transformation_mode == 'NUMBER':
                        verts = number_transform(tris, transformation, verts, np_mask, use_mask, iterations, coeff)
                    else:
                        verts = scalar_field_transform(tris, transformation, verts, np_mask, use_mask, iterations, coeff)
                else:
                    raise Exception('Transformation along normal is not implemented for Point Clouds')
            if geo_type == 'TRIS':
                new_mesh.vertices = o3d.utility.Vector3dVector(verts)
            else:
                new_mesh.points = o3d.utility.Vector3dVector(verts)

            mesh_out.append(new_mesh)


        return mesh_out



def register():
    bpy.utils.register_class(SvO3Transform)

def unregister():
    bpy.utils.unregister_class(SvO3Transform)
