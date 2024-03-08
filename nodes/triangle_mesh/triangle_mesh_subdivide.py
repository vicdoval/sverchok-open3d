
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix
import copy
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import triangle_mesh_viewer_map

if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3TriangleMeshSubdivideNode', 'O3D Triangle Mesh Subdivide', 'open3d')
else:
    class SvO3TriangleMeshSubdivideNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Triangle Mesh Subdivide
        Tooltip: Open3d Triangle Mesh Subdivide
        """
        bl_idname = 'SvO3TriangleMeshSubdivideNode'
        bl_label = 'Triangle Mesh Subdivide'
        bl_icon = 'MESH_DATA'
        viewer_map = triangle_mesh_viewer_map

        methods = [
            ('loop', "Loop", "Subdivide mesh using Loop’s algorithm", 0),
            ('midpoint', "Midpoint", "Subdivide mesh using midpoint algorithm", 1),
        ]
        method: EnumProperty(
            name="Method",
            items=methods,
            default='loop',
            update=updateNode)
        iterations: IntProperty(
            name="Iterations",
            default=1,
            update=updateNode)



        def sv_init(self, context):
            self.width = 200
            tr = self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")
            tr.is_mandatory = True
            tr.nesting_level = 1
            tr.default_mode = 'NONE'
            it = self.inputs.new('SvStringsSocket', "Iterations")
            it.prop_name = 'iterations'
            it.nesting_level = 1
            it.pre_processing = 'ONE_ITEM'
            it.default_mode = 'EMPTY_LIST'

            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'method')
            if self.method == 'vertex_clustering':
                layout.prop(self, 'contraction')

        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)
            layout.prop(self, 'list_match')

        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")

        def process_data(self, params):
            meshes = []
            for mesh, iterations in zip(*params):
                if self.method == 'loop':
                    meshes.append(mesh.subdivide_loop(number_of_iterations=iterations))
                else:
                    meshes.append(mesh.subdivide_midpoint(number_of_iterations=iterations))

            return meshes


def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshSubdivideNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshSubdivideNode)
