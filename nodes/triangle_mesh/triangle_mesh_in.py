import copy
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, numpy_full_list_cycle
from sverchok.utils.logging import info, exception
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode
from sverchok_open3d.dependencies import open3d as o3d
from sverchok.utils.dummy_nodes import add_dummy

if o3d is None:
    add_dummy('SvO3TriangleMeshInNode', 'Triangle Mesh In', 'open3d')
else:
    class SvO3TriangleMeshInNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: O3D Triangle Mesh In
        Tooltip: Open3D  Triangle Mesh In
        """
        bl_idname = 'SvO3TriangleMeshInNode'
        bl_label = 'Triangle Mesh In'
        bl_icon = 'MESH_DATA'

        def sv_init(self, context):
            self.width = 180
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")
            self.inputs.new('SvVerticesSocket', "Vertices")
            self.inputs.new('SvVerticesSocket', "Vertex Normals")
            self.inputs.new('SvColorSocket', "Vertex Colors")
            self.inputs.new('SvStringsSocket', "Faces")
            self.inputs.new('SvVerticesSocket', "Face Normals")
            self.inputs.new('SvVerticesSocket', "UV Verts")
            self.inputs.new('SvStringsSocket', "UV Faces")
            self.inputs.new('SvStringsSocket', "Material Id")
            for s in self.inputs[1:-1]:
                s.nesting_level = 3
            self.inputs[0].nesting_level = 1
            self.inputs[-1].nesting_level = 2


            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")
        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')

        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")

        def pre_setup(self):
            if not (self.inputs['Vertices'].is_linked or self.inputs['O3D Triangle Mesh'].is_linked) and self.outputs['O3D Triangle Mesh'].is_linked:
                raise Exception('"Vertices" or "O3D Triangle Mesh" inputs need to be linked')

        def process_data(self, params):

            mesh_out = []
            matched = numpy_full_list_cycle
            vec_3f = o3d.utility.Vector3dVector
            vec_3i = o3d.utility.Vector3iVector
            for base_mesh, vertices, verts_normals, verts_colors, faces, f_normals, uv_verts, uv_faces, material_id in zip(*params):
                if base_mesh:
                    mesh = copy.deepcopy(base_mesh)
                else:
                    mesh = o3d.geometry.TriangleMesh()

                if len(vertices) > 0:
                    np_vertices = np.array(vertices)
                    mesh.vertices = vec_3f(np_vertices)

                if len(faces) > 0:
                    try:
                        np_triangles = np.array(faces).astype(np.int32)
                    except ValueError:
                        raise Exception('Only Triangular Faces Accepted')
                    if np_triangles.shape[1] != 3:
                        raise Exception('Only Triangular Faces Accepted')
                    mesh.triangles = vec_3i(np_triangles)

                vert_len = len(mesh.vertices)
                tri_len = len(mesh.triangles)
                if len(verts_normals) > 0:
                    mesh.vertex_normals = vec_3f(matched(np.array(verts_normals), vert_len))

                if len(verts_colors) > 0:
                    mesh.vertex_colors = vec_3f(matched(np.array(verts_colors)[:, :3], vert_len))

                if len(f_normals) > 0:
                    mesh.triangle_normals = vec_3f(matched(np.array(f_normals), tri_len))

                if len(uv_verts) > 0 and len(uv_faces) > 0:
                    np_uv_faces = np.array(uv_faces)
                    np_uv_verts = np.array(uv_verts)
                    uvs_0 = np_uv_verts[np_uv_faces][:, :, :2]
                    uvs = o3d.utility.Vector2dVector(matched(uvs_0.reshape(-1, 2), tri_len))
                    mesh.triangle_uvs = uvs
                if len(material_id) > 0:
                    mesh.triangle_material_ids = o3d.utility.IntVector(matched(np.array(material_id), tri_len))
                mesh_out.append(mesh)

            return mesh_out




def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshInNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshInNode)
