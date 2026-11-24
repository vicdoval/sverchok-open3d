import bpy
import numpy as np
from bpy.props import BoolVectorProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.sv_mesh_utils import polygons_to_edges_np

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import calc_normals


OUTPUT_COUNT = 11


def _to_output(array, output_numpy):
    return array if output_numpy else array.tolist()


def _map_geometry_tree(data, geometry_type, func):
    """
    Recursively map a function over Open3D geometry atoms.

    Supports regular and irregular nesting, for example::

        [[mesh_a, mesh_b], mesh_c]
    """
    if isinstance(data, geometry_type):
        return func(data)

    if isinstance(data, (list, tuple)):
        return [
            _map_geometry_tree(item, geometry_type, func)
            for item in data
        ]

    raise TypeError(
        "Inappropriate argument type: "
        f"'{type(data).__module__}.{type(data).__name__}' "
        "is not an Open3D TriangleMesh or a list/tuple containing TriangleMeshes"
    )


def _split_result_tree(tree, outputs_num):
    """
    Split a nested tree of output tuples into parallel output trees.

    NumPy arrays are output leaves and are never traversed.
    """
    if isinstance(tree, tuple) and len(tree) == outputs_num:
        return tree

    if isinstance(tree, list):
        if not tree:
            return tuple([] for _ in range(outputs_num))

        split_items = [_split_result_tree(item, outputs_num) for item in tree]
        return tuple(
            [item[output_index] for item in split_items]
            for output_index in range(outputs_num)
        )

    raise TypeError(
        "Unexpected recursive result type: "
        f"{type(tree).__name__}. Expected list or {outputs_num}-tuple."
    )


def _triangle_areas(vertices, triangles):
    tri_verts = vertices[triangles]
    cross = np.cross(
        tri_verts[:, 1] - tri_verts[:, 0],
        tri_verts[:, 2] - tri_verts[:, 0],
    )
    return 0.5 * np.linalg.norm(cross, axis=1)


def _triangle_centers(vertices, triangles):
    return vertices[triangles].mean(axis=1)


class SV_MT_O3TriangleMeshOutNumpyOutputs(bpy.types.Menu):
    bl_idname = "SV_MT_o3_triangle_mesh_out_numpy_outputs"
    bl_label = "Output NumPy"

    def draw(self, context):
        space = context.space_data
        tree = getattr(space, "edit_tree", None)
        node = tree.nodes.active if tree else None

        if node is None or node.bl_idname != "SvO3TriangleMeshOutNode":
            self.layout.label(text="Select a Triangle Mesh Out node")
            return

        for index, socket in enumerate(node.outputs):
            self.layout.prop(
                node,
                "out_np",
                index=index,
                text=socket.name,
                toggle=True,
            )


class SvO3TriangleMeshOutNode(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: O3D Triangle Mesh Decompose
    Tooltip: Convert an Open3D Triangle Mesh to Sverchok data
    """

    bl_idname = "SvO3TriangleMeshOutNode"
    bl_label = "Triangle Mesh Out"
    bl_icon = "MESH_DATA"
    sv_dependencies = ["open3d"]

    out_np: BoolVectorProperty(
        name="Output NumPy",
        description="Output NumPy arrays for the selected outputs",
        size=OUTPUT_COUNT,
        default=(False,) * OUTPUT_COUNT,
        update=updateNode,
    )

    def sv_init(self, context):
        self.inputs.new(
            "SvO3TriangleMeshSocket", "O3D Triangle Mesh"
        ).is_mandatory = True

        self.outputs.new("SvVerticesSocket", "Vertices")
        self.outputs.new("SvStringsSocket", "Edges")
        self.outputs.new("SvStringsSocket", "Faces")
        self.outputs.new("SvVerticesSocket", "Vertex Normal")
        self.outputs.new("SvColorSocket", "Vertex Color")
        self.outputs.new("SvVerticesSocket", "Face Normal")
        self.outputs.new("SvVerticesSocket", "Face Center")
        self.outputs.new("SvStringsSocket", "Face Area")
        self.outputs.new("SvVerticesSocket", "UV Verts")
        self.outputs.new("SvStringsSocket", "UV Faces")
        self.outputs.new("SvStringsSocket", "Material Id")

    def draw_buttons_ext(self, context, layout):
        layout.label(text="Output NumPy:")
        column = layout.column()

        for index, socket in enumerate(self.outputs):
            column.prop(
                self,
                "out_np",
                index=index,
                text=socket.name,
                toggle=True,
            )

    def rclick_menu(self, context, layout):
        layout.menu(
            SV_MT_O3TriangleMeshOutNumpyOutputs.bl_idname,
            text="Output NumPy",
        )

    def process(self):
        input_socket = self.inputs["O3D Triangle Mesh"]

        if not input_socket.is_linked:
            return

        linked = tuple(socket.is_linked for socket in self.outputs)
        if not any(linked):
            return

        meshes = input_socket.sv_get(deepcopy=False)

        if isinstance(meshes, o3d.geometry.TriangleMesh):
            meshes = [meshes]

        def convert_mesh(mesh):
            values = [[] for _ in range(OUTPUT_COUNT)]

            vertices = np.asarray(mesh.vertices)
            has_triangles = mesh.has_triangles()
            triangles = (
                np.asarray(mesh.triangles)
                if has_triangles
                else None
            )

            if linked[0]:
                values[0] = _to_output(
                    vertices,
                    self.out_np[0],
                )

            if has_triangles:
                if linked[1]:
                    values[1] = polygons_to_edges_np(
                        [triangles],
                        unique_edges=True,
                        output_numpy=self.out_np[1],
                    )[0]

                if linked[2]:
                    values[2] = _to_output(
                        triangles,
                        self.out_np[2],
                    )

            need_vertex_normals = linked[3]
            need_face_normals = linked[5]

            calculated_vertex_normals = None
            calculated_face_normals = None

            if has_triangles:
                missing_vertex_normals = (
                    need_vertex_normals
                    and not mesh.has_vertex_normals()
                )
                missing_face_normals = (
                    need_face_normals
                    and not mesh.has_triangle_normals()
                )

                if missing_vertex_normals:
                    (
                        calculated_face_normals,
                        calculated_vertex_normals,
                    ) = calc_normals(
                        mesh,
                        v_normals=True,
                    )
                elif missing_face_normals:
                    calculated_face_normals = calc_normals(
                        mesh,
                        v_normals=False,
                    )

            if need_vertex_normals:
                if mesh.has_vertex_normals():
                    values[3] = _to_output(
                        np.asarray(mesh.vertex_normals),
                        self.out_np[3],
                    )
                elif calculated_vertex_normals is not None:
                    values[3] = _to_output(
                        calculated_vertex_normals,
                        self.out_np[3],
                    )

            if linked[4] and mesh.has_vertex_colors():
                colors = np.asarray(mesh.vertex_colors)
                colors_rgba = np.ones(
                    (colors.shape[0], 4),
                    dtype=colors.dtype,
                )
                colors_rgba[:, :3] = colors
                values[4] = _to_output(
                    colors_rgba,
                    self.out_np[4],
                )

            if need_face_normals:
                if mesh.has_triangle_normals():
                    values[5] = _to_output(
                        np.asarray(mesh.triangle_normals),
                        self.out_np[5],
                    )
                elif calculated_face_normals is not None:
                    values[5] = _to_output(
                        calculated_face_normals,
                        self.out_np[5],
                    )

            if linked[6] and has_triangles:
                values[6] = _to_output(
                    _triangle_centers(
                        vertices,
                        triangles,
                    ),
                    self.out_np[6],
                )

            if linked[7] and has_triangles:
                values[7] = _to_output(
                    _triangle_areas(
                        vertices,
                        triangles,
                    ),
                    self.out_np[7],
                )

            if mesh.has_triangle_uvs() and (
                linked[8] or linked[9]
            ):
                uvs = np.asarray(mesh.triangle_uvs)

                if linked[8]:
                    uv_vertices = np.zeros(
                        (uvs.shape[0], 3),
                        dtype=uvs.dtype,
                    )
                    uv_vertices[:, :2] = uvs
                    values[8] = _to_output(
                        uv_vertices,
                        self.out_np[8],
                    )

                if linked[9]:
                    uv_faces = np.arange(
                        uvs.shape[0],
                        dtype=np.int64,
                    ).reshape(-1, 3)
                    values[9] = _to_output(
                        uv_faces,
                        self.out_np[9],
                    )

            if (
                linked[10]
                and mesh.has_triangle_material_ids()
            ):
                values[10] = _to_output(
                    np.asarray(
                        mesh.triangle_material_ids
                    ),
                    self.out_np[10],
                )

            return tuple(values)

        result_tree = _map_geometry_tree(
            meshes,
            o3d.geometry.TriangleMesh,
            convert_mesh,
        )

        results = _split_result_tree(
            result_tree,
            OUTPUT_COUNT,
        )

        for socket, data in zip(self.outputs, results):
            if socket.is_linked:
                socket.sv_set(data)


classes = (
    SV_MT_O3TriangleMeshOutNumpyOutputs,
    SvO3TriangleMeshOutNode,
)

register, unregister = bpy.utils.register_classes_factory(classes)
