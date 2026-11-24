import bpy
import numpy as np
from bpy.props import EnumProperty, FloatProperty, IntProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, list_match_func, list_match_modes

from sverchok_open3d.dependencies import open3d as o3d


OUTPUT_COUNT = 4


def update_sockets(self, context):
    """Show only the parameter sockets used by the selected method."""
    if not self.inputs:
        return

    statistical = self.method == "STATISTICAL"

    socket_visibility = {
        "Neighbors": statistical,
        "Std Ratio": statistical,
        "Points": not statistical,
        "Radius": not statistical,
    }

    for socket_name, visible in socket_visibility.items():
        socket = self.inputs.get(socket_name)
        if socket is not None:
            socket.hide = not visible

    updateNode(self, context)


def _validate_statistical(nb_neighbors, std_ratio):
    nb_neighbors = int(nb_neighbors)
    std_ratio = float(std_ratio)

    if nb_neighbors < 1:
        raise ValueError("Neighbors must be greater than or equal to 1")
    if std_ratio <= 0.0:
        raise ValueError("Std Ratio must be greater than 0")

    return nb_neighbors, std_ratio


def _validate_radius(nb_points, radius):
    nb_points = int(nb_points)
    radius = float(radius)

    if nb_points < 1:
        raise ValueError("Points must be greater than or equal to 1")
    if radius <= 0.0:
        raise ValueError("Radius must be greater than 0")

    return nb_points, radius


def _is_sequence(value):
    if isinstance(value, (list, tuple)):
        return True
    return isinstance(value, np.ndarray) and value.ndim > 0


def _as_list(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _is_pointcloud_level(value):
    """
    True when value is already at the functional PointCloud level.

    A naked PointCloud or a flat list of PointClouds is functional.
    Lists containing sub-lists are structural nesting.
    """
    if isinstance(value, o3d.geometry.PointCloud):
        return True

    if isinstance(value, (list, tuple)):
        return all(
            isinstance(item, o3d.geometry.PointCloud)
            for item in value
        )

    return False


def _is_numeric_level(value):
    """
    True for a scalar or a flat sequence of scalar values.

    Nested lists/tuples and multidimensional NumPy arrays represent a higher
    Sverchok nesting level.
    """
    if isinstance(value, np.ndarray):
        return value.ndim <= 1

    if not isinstance(value, (list, tuple)):
        return True

    return all(not _is_sequence(item) for item in value)


def _remove_outliers(point_cloud, value_1, value_2, method):
    """Apply one Open3D outlier-removal operation to one PointCloud."""
    if method == "STATISTICAL":
        nb_neighbors, std_ratio = _validate_statistical(
            value_1,
            value_2,
        )

        inlier_cloud, indices = point_cloud.remove_statistical_outlier(
            nb_neighbors=nb_neighbors,
            std_ratio=std_ratio,
        )

    else:
        nb_points, radius = _validate_radius(
            value_1,
            value_2,
        )

        inlier_cloud, indices = point_cloud.remove_radius_outlier(
            nb_points=nb_points,
            radius=radius,
        )

    indices = [int(index) for index in indices]

    outlier_cloud = point_cloud.select_by_index(
        indices,
        invert=True,
    )

    mask = [False] * len(point_cloud.points)
    for index in indices:
        mask[index] = True

    return (
        inlier_cloud,
        outlier_cloud,
        indices,
        mask,
    )


def _process_matched_tree(
    point_clouds,
    parameter_1,
    parameter_2,
    method,
    matching_f,
):
    """
    Recursively process arbitrary PointCloud nesting with Sverchok List Match.

    PointCloud objects are atomic. A standard numeric socket wrapper such as
    ``[[30]]`` is consumed without creating an extra output nesting level.

    Examples with REPEAT::

        [A] + [[30]]              -> [f(A, 30)]
        [A, B] + [[10, 20]]      -> [f(A, 10), f(B, 20)]
        [[A, B], [C]] + [[30]]   -> [[f(A, 30), f(B, 30)], [f(C, 30)]]
        [[A, B], C] + [[30]]     -> [[f(A, 30), f(B, 30)], f(C, 30)]
    """
    pointcloud_is_atom = isinstance(
        point_clouds,
        o3d.geometry.PointCloud,
    )

    functional = (
        _is_pointcloud_level(point_clouds),
        _is_numeric_level(parameter_1),
        _is_numeric_level(parameter_2),
    )

    if all(functional):
        clouds = (
            [point_clouds]
            if pointcloud_is_atom
            else _as_list(point_clouds)
        )
        values_1 = _as_list(parameter_1)
        values_2 = _as_list(parameter_2)

        clouds, values_1, values_2 = matching_f(
            [clouds, values_1, values_2]
        )

        results = [
            _remove_outliers(
                cloud,
                value_1,
                value_2,
                method,
            )
            for cloud, value_1, value_2 in zip(
                clouds,
                values_1,
                values_2,
            )
        ]

        # A naked PointCloud is a structural leaf. If parameter matching does
        # not expand it, return the tuple directly so irregular input nesting
        # such as [[A, B], C] is preserved exactly.
        if pointcloud_is_atom and len(results) == 1:
            return results[0]

        return results

    prepared = []
    raw_values = (
        point_clouds,
        parameter_1,
        parameter_2,
    )

    for value, is_functional in zip(raw_values, functional):
        if is_functional:
            prepared.append([value])
        else:
            prepared.append(_as_list(value))

    matched = matching_f(prepared)

    children = [
        _process_matched_tree(
            child_clouds,
            child_value_1,
            child_value_2,
            method,
            matching_f,
        )
        for child_clouds, child_value_1, child_value_2 in zip(*matched)
    ]

    # If PointCloud data is already functional, recursion was caused only by
    # a higher numeric nesting level. Sverchok numeric sockets normally add a
    # single-item outer wrapper; consume that wrapper instead of reproducing it
    # in the outputs.
    nonfunctional_parameter_lengths = [
        len(_as_list(value))
        for value, is_functional in zip(
            (parameter_1, parameter_2),
            functional[1:],
        )
        if not is_functional
    ]

    if (
        functional[0]
        and len(children) == 1
        and nonfunctional_parameter_lengths
        and max(nonfunctional_parameter_lengths) == 1
    ):
        return children[0]

    return children


def _split_result_tree(tree):
    """
    Split a nested tree of result tuples into four parallel output trees.

    Only structural Python lists are traversed. PointClouds, indices and masks
    remain leaf payloads.
    """
    if isinstance(tree, tuple) and len(tree) == OUTPUT_COUNT:
        return tree

    if isinstance(tree, list):
        if not tree:
            return tuple([] for _ in range(OUTPUT_COUNT))

        split_items = [_split_result_tree(item) for item in tree]

        return tuple(
            [item[output_index] for item in split_items]
            for output_index in range(OUTPUT_COUNT)
        )

    raise TypeError(
        "Unexpected result type: "
        f"{type(tree).__module__}.{type(tree).__name__}"
    )


class SvO3PointCloudOutlierRemovalNode(
    SverchCustomTreeNode,
    bpy.types.Node,
):
    """
    Remove statistical or radius-based outliers from Open3D PointClouds.

    Supports arbitrary and irregular PointCloud nesting. List Match is applied
    at the corresponding functional level and output nesting is preserved.
    """

    bl_idname = "SvO3PointCloudOutlierRemovalNode"
    bl_label = "Point Cloud Outlier Removal"
    bl_icon = "OUTLINER_DATA_POINTCLOUD"
    sv_dependencies = ["open3d"]

    method: EnumProperty(
        name="Method",
        description="Outlier removal method",
        items=[
            (
                "STATISTICAL",
                "Statistical",
                "Remove points whose mean neighbor distance is outside "
                "the selected standard-deviation ratio",
            ),
            (
                "RADIUS",
                "Radius",
                "Remove points that do not have enough neighbors "
                "inside the selected radius",
            ),
        ],
        default="STATISTICAL",
        update=update_sockets,
    )

    nb_neighbors: IntProperty(
        name="Neighbors",
        description="Number of neighbors used to estimate the mean distance",
        default=30,
        min=1,
        update=updateNode,
    )

    std_ratio: FloatProperty(
        name="Std Ratio",
        description="Standard deviation ratio used by the statistical filter",
        default=2.0,
        min=0.000001,
        update=updateNode,
    )

    nb_points: IntProperty(
        name="Points",
        description="Minimum number of points required inside the radius",
        default=16,
        min=1,
        update=updateNode,
    )

    radius: FloatProperty(
        name="Radius",
        description="Neighborhood radius",
        default=0.05,
        min=0.000001,
        update=updateNode,
    )

    list_match: EnumProperty(
        name="List Match",
        description="How inputs of different list lengths are matched",
        items=list_match_modes,
        default="REPEAT",
        update=updateNode,
    )

    def sv_init(self, context):
        self.inputs.new(
            "SvO3PointCloudSocket",
            "Point Cloud",
        ).is_mandatory = True

        socket = self.inputs.new(
            "SvStringsSocket",
            "Neighbors",
        )
        socket.prop_name = "nb_neighbors"

        socket = self.inputs.new(
            "SvStringsSocket",
            "Std Ratio",
        )
        socket.prop_name = "std_ratio"

        socket = self.inputs.new(
            "SvStringsSocket",
            "Points",
        )
        socket.prop_name = "nb_points"

        socket = self.inputs.new(
            "SvStringsSocket",
            "Radius",
        )
        socket.prop_name = "radius"

        self.outputs.new(
            "SvO3PointCloudSocket",
            "Point Cloud",
        )
        self.outputs.new(
            "SvO3PointCloudSocket",
            "Outliers",
        )
        self.outputs.new(
            "SvStringsSocket",
            "Indices",
        )
        self.outputs.new(
            "SvStringsSocket",
            "Mask",
        )

        update_sockets(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "method",
            text="Method",
        )

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)
        layout.prop(
            self,
            "list_match",
            text="List Match",
        )

    def rclick_menu(self, context, layout):
        layout.prop_menu_enum(
            self,
            "method",
            text="Method",
        )
        layout.prop_menu_enum(
            self,
            "list_match",
            text="List Match",
        )

    def process(self):
        if not self.inputs["Point Cloud"].is_linked:
            return

        if not any(socket.is_linked for socket in self.outputs):
            return

        point_clouds = self.inputs["Point Cloud"].sv_get(
            deepcopy=False
        )

        # Keep Sverchok's normal object-list convention even if an upstream
        # custom socket provides a naked PointCloud.
        if isinstance(
            point_clouds,
            o3d.geometry.PointCloud,
        ):
            point_clouds = [point_clouds]

        if self.method == "STATISTICAL":
            parameter_1 = self.inputs["Neighbors"].sv_get(
                default=[[self.nb_neighbors]],
                deepcopy=False,
            )
            parameter_2 = self.inputs["Std Ratio"].sv_get(
                default=[[self.std_ratio]],
                deepcopy=False,
            )
        else:
            parameter_1 = self.inputs["Points"].sv_get(
                default=[[self.nb_points]],
                deepcopy=False,
            )
            parameter_2 = self.inputs["Radius"].sv_get(
                default=[[self.radius]],
                deepcopy=False,
            )

        result_tree = _process_matched_tree(
            point_clouds,
            parameter_1,
            parameter_2,
            self.method,
            list_match_func[self.list_match],
        )

        inliers, outliers, indices, mask = _split_result_tree(
            result_tree
        )

        if self.outputs["Point Cloud"].is_linked:
            self.outputs["Point Cloud"].sv_set(inliers)

        if self.outputs["Outliers"].is_linked:
            self.outputs["Outliers"].sv_set(outliers)

        if self.outputs["Indices"].is_linked:
            self.outputs["Indices"].sv_set(indices)

        if self.outputs["Mask"].is_linked:
            self.outputs["Mask"].sv_set(mask)


def register():
    bpy.utils.register_class(
        SvO3PointCloudOutlierRemovalNode
    )


def unregister():
    bpy.utils.unregister_class(
        SvO3PointCloudOutlierRemovalNode
    )
