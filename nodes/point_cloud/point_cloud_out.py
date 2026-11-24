import bpy
import numpy as np
from bpy.props import BoolProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

from sverchok_open3d.dependencies import open3d as o3d


OUTPUT_COUNT = 4


def _to_output(array, output_numpy):
    return array if output_numpy else array.tolist()


def _map_geometry_tree(data, geometry_type, func):
    """
    Recursively map a function over Open3D geometry atoms.

    Unlike Sverchok's generic nesting helpers this supports irregular trees,
    for example::

        [[geometry_a, geometry_b], geometry_c]

    Open3D geometries are always treated as atomic values.
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
        "is not an Open3D PointCloud or a list/tuple containing PointClouds"
    )


def _split_result_tree(tree, outputs_num):
    """
    Split a nested tree of output tuples into parallel output trees.

    Only the tuples produced by the geometry converter are treated as leaves.
    NumPy arrays are never traversed.
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


class SvO3PointCloudOutNode(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Point Cloud decompose
    Tooltip: Convert an Open3D Point Cloud to Sverchok data
    """

    bl_idname = "SvO3PointCloudOutNode"
    bl_label = "Point Cloud Out"
    bl_icon = "OUTLINER_OB_POINTCLOUD"
    sv_icon = "SV_O3_POINT_CLOUD_OUT"
    sv_dependencies = ["open3d"]

    output_numpy: BoolProperty(
        name="Output NumPy",
        description="Output NumPy arrays at the data leaves",
        default=False,
        update=updateNode,
    )

    def sv_init(self, context):
        self.width = 180

        self.inputs.new(
            "SvO3PointCloudSocket", "O3D Point Cloud"
        ).is_mandatory = True

        self.outputs.new("SvVerticesSocket", "Vertices")
        self.outputs.new("SvVerticesSocket", "Normals")
        self.outputs.new("SvColorSocket", "Colors")
        self.outputs.new("SvStringsSocket", "Nearest Neighbor Distance")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "output_numpy")

    def rclick_menu(self, context, layout):
        layout.prop(
            self,
            "output_numpy",
            text="Output NumPy",
            toggle=True,
        )

    def process(self):
        input_socket = self.inputs["O3D Point Cloud"]

        if not input_socket.is_linked:
            return

        linked = tuple(socket.is_linked for socket in self.outputs)
        if not any(linked):
            return

        point_clouds = input_socket.sv_get(deepcopy=False)

        # Keep the Sverchok object level even if a custom upstream socket
        # happens to provide a naked PointCloud.
        if isinstance(point_clouds, o3d.geometry.PointCloud):
            point_clouds = [point_clouds]

        def convert_point_cloud(pcd):
            values = [[] for _ in range(OUTPUT_COUNT)]

            if linked[0]:
                values[0] = _to_output(
                    np.asarray(pcd.points),
                    self.output_numpy,
                )

            if linked[1] and pcd.has_normals():
                values[1] = _to_output(
                    np.asarray(pcd.normals),
                    self.output_numpy,
                )

            if linked[2] and pcd.has_colors():
                colors = np.asarray(pcd.colors)
                colors_rgba = np.ones(
                    (colors.shape[0], 4),
                    dtype=colors.dtype,
                )
                colors_rgba[:, :3] = colors
                values[2] = _to_output(
                    colors_rgba,
                    self.output_numpy,
                )

            if linked[3]:
                distances = np.asarray(
                    pcd.compute_nearest_neighbor_distance()
                )
                values[3] = _to_output(
                    distances,
                    self.output_numpy,
                )

            return tuple(values)

        result_tree = _map_geometry_tree(
            point_clouds,
            o3d.geometry.PointCloud,
            convert_point_cloud,
        )

        results = _split_result_tree(
            result_tree,
            OUTPUT_COUNT,
        )

        for socket, data in zip(self.outputs, results):
            if socket.is_linked:
                socket.sv_set(data)


def register():
    bpy.utils.register_class(SvO3PointCloudOutNode)


def unregister():
    bpy.utils.unregister_class(SvO3PointCloudOutNode)
