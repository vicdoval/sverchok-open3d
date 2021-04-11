
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix
import copy
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.logging import info, exception
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode
from sverchok.utils.dummy_nodes import add_dummy

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import triangle_mesh_viewer_map


if o3d is None:
    add_dummy('SvO3TriangleMeshSharpenNode', 'O3D Triangle Mesh Sharpen', 'open3d')
else:
    class SvO3TriangleMeshSharpenNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Triangle Mesh Sharpen
        Tooltip: Open3d Triangle Mesh Sharpen
        """
        bl_idname = 'SvO3TriangleMeshSharpenNode'
        bl_label = 'Triangle Mesh Sharpen'
        bl_icon = 'MESH_DATA'
        viewer_map = triangle_mesh_viewer_map

        iterations: IntProperty(
            name="Iterations",
            default=1,
            min=0,
            update=updateNode)
        strength: FloatProperty(
            name="Strength",
            default=1,
            update=updateNode)


        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True
            self.inputs.new('SvStringsSocket', "Iterations").prop_name = 'iterations'
            self.inputs.new('SvStringsSocket', "Strength").prop_name = 'strength'

            for s in self.inputs[1:]:
                s.nesting_level = 1
                s.pre_processing = 'ONE_ITEM'


            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')


        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")


        def process_data(self, params):

            mesh_out = []

            for mesh, iterations, strength in zip(*params):
                if iterations < 1:
                    mesh_new = mesh
                else:
                    mesh_new = mesh.filter_sharpen(number_of_iterations=iterations, strength=strength)

                mesh_out.append(mesh_new)


            return mesh_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshSharpenNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshSharpenNode)
