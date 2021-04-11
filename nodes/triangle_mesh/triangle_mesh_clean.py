
import copy
import numpy as np

import bpy
from bpy.props import BoolProperty


from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode
from sverchok.utils.dummy_nodes import add_dummy

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import clean_doubled_faces, triangle_mesh_viewer_map

if o3d is None:
    add_dummy('SvO3TriangleMeshCleanNode', 'Triangle Mesh Clean', 'open3d')
else:
    class SvO3TriangleMeshCleanNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Triangle Mesh Clean
        Tooltip: Open3d Triangle Mesh Clean
        """
        bl_idname = 'SvO3TriangleMeshCleanNode'
        bl_label = 'Triangle Mesh Clean'
        bl_icon = 'MESH_DATA'

        viewer_map = triangle_mesh_viewer_map

        normalize_normals: BoolProperty(
            name="Normalize Normals",
            description="Orient Triangles Outwards",
            default=False,
            update=updateNode)
        orient_triangles: BoolProperty(
            name="Orient Triangles",
            description="Orient Triangles Outwards",
            default=False,
            update=updateNode)
        remove_non_manifold_edges: BoolProperty(
            name="Non Manifold Edges",
            description="Remove Non Manifold Edges",
            default=False,
            update=updateNode)
        remove_duplicated_vertices: BoolProperty(
            name="Duplicated Verts",
            description="Remove Duplicated Verts",
            default=False,
            update=updateNode)
        remove_degenerate_triangles: BoolProperty(
            name="Degenrated Verts",
            description="Remove Degenrated Verts",
            default=False,
            update=updateNode)
        remove_duplicated_triangles: BoolProperty(
            name="Duplicated Triangles",
            description="Remove Duplicated Triangles",
            default=False,
            update=updateNode)
        remove_unreferenced_vertices: BoolProperty(
            name="Unreferenced Vertices",
            description="Remove Unreferenced Vertices",
            default=False,
            update=updateNode)

        def sv_init(self, context):
            self.width = 180
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True

            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'normalize_normals')
            layout.prop(self, 'orient_triangles')
            layout.label(text='Remove:')
            layout.prop(self, 'remove_non_manifold_edges')
            layout.prop(self, 'remove_duplicated_vertices')
            layout.prop(self, 'remove_degenerate_triangles')
            layout.prop(self, 'remove_duplicated_triangles')
            layout.prop(self, 'remove_unreferenced_vertices')

        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)

        def process_data(self, params):

            mesh_out = []

            for mesh in params[0]:
                mn = copy.deepcopy(mesh)

                if self.normalize_normals:
                    mn = mn.normalize_normals()
                if self.orient_triangles:
                    mn.orient_triangles()
                if self.remove_duplicated_vertices:
                    mn = mn.remove_duplicated_vertices()
                if self.remove_non_manifold_edges:
                    mn = mn.remove_non_manifold_edges()
                if self.remove_degenerate_triangles:
                    mn = mn.remove_degenerate_triangles()
                if self.remove_duplicated_triangles:
                    # this function does not seem to work
                    # mn = mn.remove_duplicated_triangles()
                    clean_doubled_faces(mn)
                if self.remove_unreferenced_vertices:
                    mn = mn.remove_unreferenced_vertices()


                mesh_out.append(mn)


            return mesh_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshCleanNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshCleanNode)
