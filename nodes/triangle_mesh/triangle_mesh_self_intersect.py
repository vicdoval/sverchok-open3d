
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
    add_dummy('SvO3TriangleMeshSelfIntersectNode', 'O3D Triangle Mesh Sharpen', 'open3d')
else:
    class SvO3TriangleMeshSelfIntersectNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Triangle Mesh Sharpen
        Tooltip: Open3d Triangle Mesh Sharpen
        """
        bl_idname = 'SvO3TriangleMeshSelfIntersectNode'
        bl_label = 'Triangle Mesh Self Intersect'
        bl_icon = 'MESH_DATA'


        iterations: IntProperty(
            name="Iterations",
            default=1,
            min=0,
            update=updateNode)
        strength: FloatProperty(
            name="Strength",
            default=1,
            update=updateNode)
        output_numpy: BoolProperty(
            name="Output Numpy",
            default=False,
            update=updateNode)


        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True

            self.outputs.new('SvStringsSocket', "Is Self-intersecting")
            self.outputs.new('SvStringsSocket', "Faces Pairs")

        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')
            layout.prop(self, 'output_numpy')


        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")
            layout.prop(self, 'output_numpy')


        def process_data(self, params):

            self_intersect, intersecting_tris = [], []
            for mesh in params[0]:
                is_self_intersecting = mesh.is_self_intersecting()
                self_intersect.append(is_self_intersecting)
                if is_self_intersecting:
                    interseting_tris = mesh.get_self_intersecting_triangles()
                    if self.output_numpy:
                        intersecting_tris.append(np.asarray(interseting_tris))
                    else:
                        intersecting_tris.append(np.asarray(interseting_tris).tolist())
                else:
                    intersecting_tris.append([])




            return self_intersect, intersecting_tris



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshSelfIntersectNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshSelfIntersectNode)
