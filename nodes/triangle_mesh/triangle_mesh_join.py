
import numpy as np
import copy
import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.sv_logging import sv_logger
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import triangle_mesh_viewer_map

if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3TriangleMeshJoinNode', 'Triangle Mesh In', 'open3d')
else:
    class SvO3TriangleMeshJoinNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: O3D Triangle Mesh Join
        Tooltip: Open3D  Triangle Mesh Join
        """
        bl_idname = 'SvO3TriangleMeshJoinNode'
        bl_label = 'Triangle Mesh Join'
        bl_icon = 'MESH_DATA'

        viewer_map = triangle_mesh_viewer_map

        compute_vertex_normals: BoolProperty(
            name="compute Vertex Normals",
            default=False,
            update=updateNode)
        compute_faces_normals: BoolProperty(
            name="compute Faces Normals",
            default=False,
            update=updateNode)
        def sv_init(self, context):
            self.width = 200
            mesh = self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")
            mesh.is_mandatory = True
            mesh.nesting_level = 1
            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'compute_vertex_normals')
            layout.prop(self, 'compute_faces_normals')

        def process_data(self, params):
            mesh_in = params[0]
            mesh_out = []
            new_mesh = copy.deepcopy(mesh_in[0])
            new_mesh.vertices = o3d.utility.Vector3dVector(
                np.concatenate([np.asarray(mesh.vertices) for mesh in mesh_in])
                )
            triangles_len = np.cumsum([0]+[len(mesh.vertices) for mesh in mesh_in])

            new_mesh.triangles = o3d.utility.Vector3iVector(
                np.concatenate([np.asarray(mesh.triangles)+offset for mesh, offset in zip(mesh_in, triangles_len)])
                )

            has_triangle_normals = [mesh.has_triangle_normals for mesh in mesh_in]
            if all(has_triangle_normals):
                new_mesh.triangle_normals = o3d.utility.Vector3dVector(
                    np.concatenate([np.asarray(mesh.triangle_normals)  for mesh in mesh_in])
                    )
            elif self.compute_faces_normals:
                new_mesh.compute_triangle_normals(normalized=True)
            #
            has_vertex_normals = [mesh.has_vertex_normals() for mesh in mesh_in]
            if all(has_vertex_normals):
                new_mesh.triangle_normals = o3d.utility.Vector3dVector(
                    np.concatenate([np.asarray(mesh.vertex_normals)  for mesh in mesh_in])
                    )
            elif self.compute_vertex_normals:
                new_mesh.compute_vertex_normals(normalized=True)

            has_vertex_colors = [mesh.has_vertex_colors() for mesh in mesh_in]
            if all(has_vertex_colors):
                new_mesh.vertex_colors = o3d.utility.Vector3dVector(
                    np.concatenate([np.asarray(mesh.vertex_colors)  for mesh in mesh_in])
                    )
            elif any(has_vertex_colors):
                new_mesh.vertex_colors = o3d.utility.Vector3dVector(
                    np.concatenate([np.asarray(mesh.vertex_colors) if mesh.has_vertex_colors else np.zeros((len(mesh.vertices),3), dtype='float')
                                    for mesh in mesh_in])
                    )
            has_triangle_uvs = [mesh.has_triangle_uvs() for mesh in mesh_in]
            if all(has_triangle_uvs):
                new_mesh.triangle_uvs = o3d.utility.Vector2dVector(
                    np.concatenate([np.asarray(mesh.triangle_uvs)  for mesh in mesh_in])
                    )
            elif any(has_triangle_uvs):
                new_mesh.triangle_uvs = o3d.utility.Vector2dVector(
                    np.concatenate([np.asarray(mesh.triangle_uvs) if mesh.has_triangle_uvs else np.zeros((len(mesh.triangles)*3, 2), dtype='float')
                    for mesh in mesh_in])
                    )

            has_triangle_material_ids = [mesh.has_triangle_material_ids() for mesh in mesh_in]
            if all(has_triangle_material_ids):
                new_mesh.triangle_material_ids = o3d.utility.IntVector(
                    np.concatenate([np.asarray(mesh.triangle_material_ids)  for mesh in mesh_in])
                    )
            elif any(has_triangle_material_ids):
                new_mesh.triangle_material_ids = o3d.utility.IntVector(
                    np.concatenate([np.asarray(mesh.triangle_material_ids) if mesh.has_triangle_uvs else np.zeros(len(mesh.triangles), dtype='int')
                    for mesh in mesh_in])
                    )

            return [new_mesh]



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshJoinNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshJoinNode)
