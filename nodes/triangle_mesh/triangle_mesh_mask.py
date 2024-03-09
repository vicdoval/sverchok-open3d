
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
import copy
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, numpy_full_list
from sverchok.utils.sv_logging import sv_logger
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import triangle_mesh_viewer_map

def calc_full_mask(mask, index, filter_method, invert, length):
    if filter_method == 'INDEX':
        if invert:
            full_mask = np.zeros(length, dtype='bool')
            full_mask[np.array(index)] = True
        else:
            full_mask = np.ones(length, dtype='bool')
            full_mask[np.array(index)] = False
    else:
        if invert:
            full_mask = numpy_full_list(np.array(mask).astype(bool), length)
        else:
            full_mask = numpy_full_list(np.invert(np.array(mask).astype(bool)), length)
    return full_mask


class SvO3TriangleMeshMaskNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
    """
    Triggers: O3D Mesh Sampling
    Tooltip: Points over Open3d mesh. Mesh to Point Cloud
    """
    bl_idname = 'SvO3TriangleMeshMaskNode'
    bl_label = 'Triangle Mesh Mask'
    bl_icon = 'MESH_DATA'
    sv_dependencies = ['open3d']
    
    viewer_map = triangle_mesh_viewer_map

    methods = [
        ('VERTS', "Verts", "Uniform Sampling", 0),
        ('TRIANGLES', "Triangles", "Poisson Disk Sampling", 1),
    ]
    filter_methods = [
        ('INDEX', "Index", "Index", 0),
        ('MASK', "Mask", "Mask", 1),
    ]
    def update_sockets(self, context):
        self.inputs['Index'].hide_safe = self.filter_method != 'INDEX'
        self.inputs['Mask'].hide_safe = self.filter_method != 'MASK'
        updateNode(self, context)
    method: EnumProperty(
        name="Method",
        items=methods,
        default='VERTS',
        update=update_sockets)
    filter_method: EnumProperty(
        name="Filter Method",
        items=filter_methods,
        default='INDEX',
        update=update_sockets)
    remove_unreferenced_vertices: BoolProperty(
        name="remove_unreferenced_vertices",
        default=False,
        update=updateNode)
    invert: BoolProperty(
        name="Invert",
        default=False,
        update=updateNode)
    index: IntProperty(
        name="Index",
        default=0,
        update=updateNode)


    def sv_init(self, context):
        self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True
        idx = self.inputs.new('SvStringsSocket', "Index")
        idx.prop_name = 'index'
        idx.nesting_level = 2

        mask = self.inputs.new('SvStringsSocket', "Mask")
        mask.hide_safe = True
        mask.nesting_level = 2

        self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'method')
        layout.prop(self, 'filter_method')
        layout.prop(self, 'invert')
        if self.method == 'TRIANGLES':
            layout.prop(self, 'remove_unreferenced_vertices')
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, 'list_match')

    def rclick_menu(self, context, layout):
        '''right click sv_menu items'''
        layout.prop_menu_enum(self, "method")
        layout.prop_menu_enum(self, "filter_method")
        layout.prop_menu_enum(self, "list_match")


    def process_data(self, params):

        mesh_out = []

        for mesh, index, mask in zip(*params):
            new_mesh = copy.deepcopy(mesh)

            if self.method == 'TRIANGLES':
                full_mask = calc_full_mask(mask, index, self.filter_method, self.invert, len(mesh.triangles))
                new_mesh.remove_triangles_by_mask(full_mask)
                if self.remove_unreferenced_vertices:
                    new_mesh.remove_unreferenced_vertices()
            else:
                full_mask = calc_full_mask(mask, index, self.filter_method, self.invert, len(mesh.vertices))
                new_mesh.remove_vertices_by_mask(full_mask)

            mesh_out.append(new_mesh)


        return mesh_out



def register():
    bpy.utils.register_class(SvO3TriangleMeshMaskNode)

def unregister():
    bpy.utils.unregister_class(SvO3TriangleMeshMaskNode)
