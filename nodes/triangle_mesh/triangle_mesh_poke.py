
import copy
import numpy as np

import bpy
from bpy.props import FloatProperty, BoolVectorProperty, BoolProperty, IntProperty
from mathutils import Matrix
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, numpy_full_list, has_element
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode
from sverchok.utils.dummy_nodes import add_dummy

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import calc_normals, calc_tris_areas

if o3d is None:
    add_dummy('SvO3TriangleMeshPokeNode', 'O3D Triangle Mesh Poke', 'open3d')
else:

    vec_3f = o3d.utility.Vector3dVector
    vec_2f = o3d.utility.Vector2dVector
    vec_3i = o3d.utility.Vector3iVector
    vec_1i = o3d.utility.IntVector

    def get_normals(triangle_mesh, np_verts, np_faces, mask):
        if triangle_mesh.has_triangle_normals():
            normals = np.asarray(triangle_mesh.triangle_normals)[mask]
        else:
            normals = calc_normals([np_verts, np_faces[mask]], v_normals=False, output_numpy=True, as_array=True)
        return normals

    def spread_vertex_attrib(triangle_mesh, np_faces_masked, attribute):
        if getattr(triangle_mesh, 'has_'+ attribute)():
            np_attrib = np.asarray(getattr(triangle_mesh, attribute))
            np_attrib_pols = np_attrib[np_faces_masked]
            attrib_center = np.sum(np_attrib_pols, axis=1) / 3
            all_attrib = np.concatenate([np_attrib, attrib_center])
            setattr(triangle_mesh, attribute, vec_3f(all_attrib))

    def spread_face_attrib(triangle_mesh, mask, attribute, attrib_len, convert_func):
        if getattr(triangle_mesh, 'has_'+ attribute)():
            np_attrib = np.asarray(getattr(triangle_mesh, attribute))
            np_attrib_masked = np_attrib[mask]
            if attrib_len == 1:
                attrib_center = np.repeat(np_attrib_masked, 3, axis=0).flatten()
            else:
                attrib_center = np.repeat(np_attrib_masked, 3, axis=0).reshape(-1, attrib_len)
            all_attrib = np.concatenate([np_attrib[np.invert(mask)], attrib_center])
            setattr(triangle_mesh, attribute, convert_func(all_attrib))

    def poke_uvs(triangle_mesh, mask):
        if triangle_mesh.has_triangle_uvs():
            uvs = np.asarray(triangle_mesh.triangle_uvs).reshape(-1, 3, 2)
            uvs_masked = uvs[mask]
            center = np.sum(uvs_masked, axis=1) / 3
            new_uvs = np.zeros((len(uvs_masked), 3, 3, 2), dtype='float')

            new_uvs[:, :, 2] = center[:, np.newaxis,:]
            for i in range(3):
                new_uvs[:, i, 0] = uvs[mask, i]
                new_uvs[:, i, 1] = uvs[mask, (i + 1) % 3]
            all_uvs = np.concatenate([uvs[np.invert(mask)].reshape(-1,2), new_uvs.reshape(-1, 2)])
            triangle_mesh.triangle_uvs = vec_2f(all_uvs)


    def triangle_mesh_poke(mesh, mask_in, offset_in, v_color, mat_id, relative_offset=False, deepcopy=True):
        if deepcopy:
            triangle_mesh = copy.deepcopy(mesh)
        else:
            triangle_mesh = mesh
        np_verts = np.asarray(triangle_mesh.vertices)

        mask = numpy_full_list(mask_in, len(triangle_mesh.triangles)).astype('bool')
        if len(offset_in) == np.sum(mask):
            offset = np.array(offset_in)[:, np.newaxis]
        elif len(offset_in) > 1:
            offset = numpy_full_list(offset_in, len(triangle_mesh.triangles))[mask, np.newaxis]
        else:
            offset = offset_in

        np_faces = np.asarray(triangle_mesh.triangles)
        faces_masked = np_faces[mask]
        v_pols = np_verts[np_faces[mask]]
        center = np.sum(v_pols, axis=1) / 3
        normals = get_normals(triangle_mesh, np_verts, np_faces, mask)
        faces_num = np_faces[mask].shape[0]
        if relative_offset:
            areas = calc_tris_areas(v_pols)
            new_vecs = center + normals * (offset* areas[:, np.newaxis])
        else:
            new_vecs = center + normals * offset
        all_vecs = np.concatenate([np_verts, new_vecs])

        new_faces = np.zeros((faces_num, 3, 3), dtype='int')

        new_faces[:, :, 2] = (np.arange(faces_num) + len(np_verts))[:, np.newaxis]
        for i in range(3):
            new_faces[:, i, 0] = np_faces[mask, i]
            new_faces[:, i, 1] = np_faces[mask, (i + 1) % 3]
        new_faces_shaped = new_faces.reshape(-1, 3)
        all_faces = np.concatenate([np_faces[np.invert(mask)], new_faces_shaped])
        if has_element(v_color):
            if triangle_mesh.has_vertex_colors():
                v_col = numpy_full_list(v_color, len(new_vecs))[:,:3]
                triangle_mesh.vertex_colors = vec_3f(np.concatenate([np.asarray(triangle_mesh.vertex_colors), v_col]))
        else:
            spread_vertex_attrib(triangle_mesh, faces_masked, 'vertex_colors')
        spread_vertex_attrib(triangle_mesh, faces_masked, 'vertex_normals')
        spread_face_attrib(triangle_mesh, mask, 'triangle_normals', 3, vec_3f)
        if len(mat_id) > 0:
            if triangle_mesh.has_triangle_material_ids():
                mat_id_shaped = numpy_full_list(mat_id, len(new_faces_shaped))
                triangle_mesh.triangle_material_ids = vec_1i(
                    np.concatenate(
                        [np.asarray(triangle_mesh.triangle_material_ids)[np.invert(mask)],
                         mat_id_shaped]
                    ))
            else:
                mat_id_shaped = numpy_full_list(mat_id, len(all_faces))
                triangle_mesh.triangle_material_ids = vec_1i(mat_id_shaped)
        else:
            spread_face_attrib(triangle_mesh, mask, 'triangle_material_ids', 1, vec_1i)
        poke_uvs(triangle_mesh, mask)
        triangle_mesh.vertices = vec_3f(all_vecs)
        triangle_mesh.triangles = vec_3i(all_faces)
        return (triangle_mesh,
                new_vecs,
                np.arange(len(np_verts), len(np_verts)+len(new_vecs)),
                np.arange(len(all_faces)-len(new_faces_shaped), len(all_faces))
                )


    class SvO3TriangleMeshPokeNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Triangle Mesh Poke
        Tooltip: Open3d Triangle Mesh Poke
        """
        bl_idname = 'SvO3TriangleMeshPokeNode'
        bl_label = 'Triangle Mesh Poke'
        bl_icon = 'MESH_DATA'


        viewer_map = [
            ("SvO3TriangleMeshOutNode", [60, 0]),
            ("SvViewerDrawMk4", [60, 0]),
            ], [
            ([0, 0], [1, 0]),
            ([1, 0], [2, 0]),
            ([1, 1], [2, 1]),
            ([1, 2], [2, 2]),
            ]
        offset: FloatProperty(
            name="Offset",
            default=1,
            update=updateNode)
        relative_offset: BoolProperty(
            name="Relative Offset",
            description='Multiply offset by the area of the triangle',
            default=False,
            update=updateNode)
        iterations: IntProperty(
            name="Iterations",
            default=1,
            update=updateNode)
        out_np: BoolVectorProperty(
            name="Ouput Numpy",
            description="Output NumPy arrays",
            # default=default_np,
            size=11, update=updateNode)


        def sv_init(self, context):
            self.width = 200
            tr = self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")
            tr.is_mandatory = True
            tr.nesting_level = 1
            tr.default_mode = 'NONE'
            self.inputs.new('SvStringsSocket', "Offset").prop_name = 'offset'
            self.inputs.new('SvStringsSocket', "Mask").default_mode = 'MASK'
            self.inputs.new('SvColorSocket', "New Vertex Color")
            self.inputs.new('SvStringsSocket', "New Material Id")


            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")
            self.outputs.new('SvVerticesSocket', "New Vertices")
            self.outputs.new('SvStringsSocket', "New Verts Idx")
            self.outputs.new('SvStringsSocket', "New Faces Idx")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'relative_offset')


        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)
            layout.prop(self, 'list_match')
            r = layout.column(align=True)
            r.label(text="Ouput Numpy:")
            for i in range(1, len(self.outputs)):
                r.prop(self, "out_np", index=i-1, text=self.outputs[i].name, toggle=True)

        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")

        def process_data(self, params):
            meshes, new_verts, new_verts_idx, new_faces_idx = [], [], [], []
            for mesh, offset, mask, v_color, mat_id  in zip(*params):

                new_mesh, vert, vert_idx, face_idx = triangle_mesh_poke(mesh,
                                                                        mask,
                                                                        offset,
                                                                        v_color,
                                                                        mat_id,
                                                                        relative_offset=self.relative_offset)
                meshes.append(new_mesh)
                new_verts.append(vert if self.out_np[0] else vert.tolist())
                new_verts_idx.append(vert_idx if self.out_np[1] else vert_idx.tolist())
                new_faces_idx.append(face_idx if self.out_np[2] else face_idx.tolist())
            return meshes, new_verts, new_verts_idx, new_faces_idx


def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshPokeNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshPokeNode)
