
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

import numpy as np
from sverchok_open3d.dependencies import open3d as o3d

if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3TriangleMeshIntersectNode', 'Triangle Mesh Simplify', 'open3d')
else:
    class SvO3TriangleMeshIntersectNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: O3D Mesh Sampling
        Tooltip: Check if two meshes intersect
        """
        bl_idname = 'SvO3TriangleMeshIntersectNode'
        bl_label = 'Triangle Mesh Intersects'
        bl_icon = 'MESH_DATA'

        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh A").is_mandatory = True
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh B").is_mandatory = True


            self.outputs.new('SvStringsSocket', "Intersect")



        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')


        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")


        def process_data(self, params):

            bool_list = []

            for mesh_a, mesh_b in zip(*params):
                bool_list.append(mesh_a.is_intersecting(mesh_b))

            return bool_list



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshIntersectNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshIntersectNode)
