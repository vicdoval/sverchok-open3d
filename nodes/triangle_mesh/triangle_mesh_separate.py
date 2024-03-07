
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix
import copy
import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.sv_logging import sv_logger
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import triangle_mesh_viewer_map

if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3TriangleMeshSeparateNode', 'O3D Triangle Mesh Separate', 'open3d')
else:
    class SvO3TriangleMeshSeparateNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Separate Loose Parts
        Tooltip: Open3d Triangle Mesh Separate Loose Parts
        """
        bl_idname = 'SvO3TriangleMeshSeparateNode'
        bl_label = 'Triangle Mesh Separate Loose'
        bl_icon = 'MESH_DATA'
        viewer_map = triangle_mesh_viewer_map
        join: BoolProperty(
            name='Flat List',
            description='Flatten all meshes to a single list of meshes',
            default=True,
            update=updateNode
        )
        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True

            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")
            self.outputs.new('SvStringsSocket', "Num of Triangles")
            self.outputs.new('SvStringsSocket', "Area")


        def draw_buttons(self, context, layout):
            layout.prop(self, 'join')


        def process_data(self, params):

            mesh_out, area_out, number_out = [], [], []
            for mesh in params[0]:
                meshes = []
                indexes, number, area = mesh.cluster_connected_triangles()
                if self.join:
                    area_out.extend(np.asarray(area).tolist())
                    number_out.extend(np.asarray(number).tolist())
                else:
                    area_out.append(np.asarray(area).tolist())
                    number_out.append(np.asarray(number).tolist())
                np_indexes = np.asarray(indexes)
                for i, a in enumerate(area):
                    new_mesh = copy.deepcopy(mesh)
                    new_mesh.remove_triangles_by_mask(np_indexes!=i)
                    new_mesh.remove_unreferenced_vertices()


                    meshes.append(new_mesh)
                if self.join:
                    mesh_out.extend(meshes)
                else:
                    mesh_out.append(meshes)

            if self.join:
                return mesh_out, [number_out], [area_out]

            return mesh_out, number_out, area_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshSeparateNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshSeparateNode)
