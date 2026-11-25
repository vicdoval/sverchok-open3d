import bpy
import numpy as np
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, list_match_func, list_match_modes

from sverchok_open3d.dependencies import open3d as o3d


METHOD_SOCKETS = {
    "MLS": {"Radius", "Max Neighbors"},
    "BILATERAL": {"Radius", "Max Neighbors", "Sigma Spatial", "Sigma Range"},
    "LAPLACIAN": {"Iterations", "Lambda", "KNN"},
    "TAUBIN": {"Iterations", "Lambda", "Mu", "KNN"},
}


def update_sockets(self, context):
    """Show only sockets used by the selected smoothing method."""
    if not self.inputs:
        return

    visible = METHOD_SOCKETS[self.method]
    for socket in self.inputs:
        if socket.name == "Point Cloud":
            continue
        socket.hide = socket.name not in visible

    updateNode(self, context)


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
    """Return True for a PointCloud or a flat list of PointClouds."""
    if isinstance(value, o3d.geometry.PointCloud):
        return True
    if isinstance(value, (list, tuple)):
        return all(isinstance(item, o3d.geometry.PointCloud) for item in value)
    return False


def _is_parameter_level(value):
    """Return True for a scalar or a flat sequence of scalars."""
    if isinstance(value, np.ndarray):
        return value.ndim <= 1
    if not isinstance(value, (list, tuple)):
        return True
    return all(not _is_sequence(item) for item in value)


def _process_geometry_tree(point_clouds, parameters, evaluate, matching_f):
    """
    Recursively process PointClouds and parameter trees.

    PointCloud objects are atomic. Sverchok List Match is applied when geometry
    and all parameters reach their functional levels. Regular and irregular
    geometry nesting are preserved.
    """
    geometry_is_atom = isinstance(point_clouds, o3d.geometry.PointCloud)

    functional = [
        _is_pointcloud_level(point_clouds),
        *(_is_parameter_level(value) for value in parameters),
    ]

    if all(functional):
        geometries = [point_clouds] if geometry_is_atom else _as_list(point_clouds)
        parameter_lists = [_as_list(value) for value in parameters]
        matched = matching_f([geometries, *parameter_lists])

        results = [
            evaluate(geometry, *values)
            for geometry, *values in zip(*matched)
        ]

        if geometry_is_atom and len(results) == 1:
            return results[0]
        return results

    values = [point_clouds, *parameters]
    prepared = [
        [value] if is_functional else _as_list(value)
        for value, is_functional in zip(values, functional)
    ]
    matched = matching_f(prepared)

    children = [
        _process_geometry_tree(
            child_geometry,
            list(child_parameters),
            evaluate,
            matching_f,
        )
        for child_geometry, *child_parameters in zip(*matched)
    ]

    # Consume Sverchok's standard one-item wrapper on numerical sockets.
    nonfunctional_parameter_lengths = [
        len(_as_list(value))
        for value, is_functional in zip(parameters, functional[1:])
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


class SvO3PointCloudSmoothNode(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Point Cloud Smooth, MLS, Laplacian, Taubin, Bilateral
    Tooltip: Smooth an Open3D Point Cloud
    """

    bl_idname = "SvO3PointCloudSmoothNode"
    bl_label = "Point Cloud Smooth"
    bl_icon = "OUTLINER_OB_POINTCLOUD"
    sv_icon = "SV_RANDOM_NUM_GEN"
    sv_dependencies = ["open3d"]

    method: EnumProperty(
        name="Method",
        items=[
            ("MLS", "MLS", "Moving Least Squares tangent-plane projection"),
            ("BILATERAL", "Bilateral", "Feature-preserving bilateral smoothing"),
            ("LAPLACIAN", "Laplacian", "Laplacian smoothing on a KNN graph"),
            ("TAUBIN", "Taubin", "Two-pass Laplacian smoothing with reduced shrinkage"),
        ],
        default="MLS",
        update=update_sockets,
    )

    radius: FloatProperty(name="Radius", default=0.05, min=0.000001, update=updateNode)
    max_neighbors: IntProperty(name="Max Neighbors", default=30, min=1, update=updateNode)
    iterations: IntProperty(name="Iterations", default=10, min=0, update=updateNode)
    filter_lambda: FloatProperty(name="Lambda", default=0.5, update=updateNode)
    filter_mu: FloatProperty(name="Mu", default=-0.53, update=updateNode)
    knn: IntProperty(name="KNN", default=20, min=1, update=updateNode)
    sigma_spatial: FloatProperty(name="Sigma Spatial", default=0.05, min=0.000001, update=updateNode)
    sigma_range: FloatProperty(name="Sigma Range", default=0.05, min=0.000001, update=updateNode)

    fixed_neighborhoods: BoolProperty(
        name="Fixed Neighborhoods",
        description="Reuse the initial KNN graph for Laplacian/Taubin smoothing",
        default=False,
        update=updateNode,
    )

    list_match: EnumProperty(
        name="List Match",
        description="How geometry and parameter lists of different lengths are matched",
        items=list_match_modes,
        default="REPEAT",
        update=updateNode,
    )

    def sv_init(self, context):
        self.width = 190

        self.inputs.new("SvO3PointCloudSocket", "Point Cloud").is_mandatory = True

        socket = self.inputs.new("SvStringsSocket", "Radius")
        socket.prop_name = "radius"

        socket = self.inputs.new("SvStringsSocket", "Max Neighbors")
        socket.prop_name = "max_neighbors"

        socket = self.inputs.new("SvStringsSocket", "Iterations")
        socket.prop_name = "iterations"

        socket = self.inputs.new("SvStringsSocket", "Lambda")
        socket.prop_name = "filter_lambda"

        socket = self.inputs.new("SvStringsSocket", "Mu")
        socket.prop_name = "filter_mu"

        socket = self.inputs.new("SvStringsSocket", "KNN")
        socket.prop_name = "knn"

        socket = self.inputs.new("SvStringsSocket", "Sigma Spatial")
        socket.prop_name = "sigma_spatial"

        socket = self.inputs.new("SvStringsSocket", "Sigma Range")
        socket.prop_name = "sigma_range"

        self.outputs.new("SvO3PointCloudSocket", "Point Cloud")
        update_sockets(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "method", text="Method")
        if self.method in {"LAPLACIAN", "TAUBIN"}:
            layout.prop(self, "fixed_neighborhoods", text="Fixed Neighborhoods")

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)
        layout.prop(self, "list_match", text="List Match")

    def rclick_menu(self, context, layout):
        layout.prop_menu_enum(self, "method", text="Method")
        layout.prop_menu_enum(self, "list_match", text="List Match")
        if self.method in {"LAPLACIAN", "TAUBIN"}:
            layout.prop(self, "fixed_neighborhoods", text="Fixed Neighborhoods")

    def _get_method_data(self):
        if self.method == "MLS":
            parameters = [
                self.inputs["Radius"].sv_get(default=[[self.radius]], deepcopy=False),
                self.inputs["Max Neighbors"].sv_get(default=[[self.max_neighbors]], deepcopy=False),
            ]

            def evaluate(point_cloud, radius, max_neighbors):
                if not hasattr(point_cloud, "smooth_mls"):
                    raise RuntimeError("Point Cloud Smooth requires Open3D 0.20 or newer")
                search_param = o3d.geometry.KDTreeSearchParamHybrid(
                    radius=float(radius), max_nn=int(max_neighbors)
                )
                return point_cloud.smooth_mls(search_param=search_param)

        elif self.method == "BILATERAL":
            parameters = [
                self.inputs["Radius"].sv_get(default=[[self.radius]], deepcopy=False),
                self.inputs["Max Neighbors"].sv_get(default=[[self.max_neighbors]], deepcopy=False),
                self.inputs["Sigma Spatial"].sv_get(default=[[self.sigma_spatial]], deepcopy=False),
                self.inputs["Sigma Range"].sv_get(default=[[self.sigma_range]], deepcopy=False),
            ]

            def evaluate(point_cloud, radius, max_neighbors, sigma_spatial, sigma_range):
                if not hasattr(point_cloud, "smooth_bilateral"):
                    raise RuntimeError("Point Cloud Smooth requires Open3D 0.20 or newer")
                search_param = o3d.geometry.KDTreeSearchParamHybrid(
                    radius=float(radius), max_nn=int(max_neighbors)
                )
                return point_cloud.smooth_bilateral(
                    search_param=search_param,
                    sigma_s=float(sigma_spatial),
                    sigma_r=float(sigma_range),
                )

        elif self.method == "LAPLACIAN":
            parameters = [
                self.inputs["Iterations"].sv_get(default=[[self.iterations]], deepcopy=False),
                self.inputs["Lambda"].sv_get(default=[[self.filter_lambda]], deepcopy=False),
                self.inputs["KNN"].sv_get(default=[[self.knn]], deepcopy=False),
            ]

            def evaluate(point_cloud, iterations, filter_lambda, knn):
                if not hasattr(point_cloud, "smooth_laplacian"):
                    raise RuntimeError("Point Cloud Smooth requires Open3D 0.20 or newer")
                return point_cloud.smooth_laplacian(
                    iterations=int(iterations),
                    lambda_=float(filter_lambda),
                    knn=int(knn),
                    use_fixed_neighborhoods=self.fixed_neighborhoods,
                )

        else:
            parameters = [
                self.inputs["Iterations"].sv_get(default=[[self.iterations]], deepcopy=False),
                self.inputs["Lambda"].sv_get(default=[[self.filter_lambda]], deepcopy=False),
                self.inputs["Mu"].sv_get(default=[[self.filter_mu]], deepcopy=False),
                self.inputs["KNN"].sv_get(default=[[self.knn]], deepcopy=False),
            ]

            def evaluate(point_cloud, iterations, filter_lambda, filter_mu, knn):
                if not hasattr(point_cloud, "smooth_taubin"):
                    raise RuntimeError("Point Cloud Smooth requires Open3D 0.20 or newer")
                return point_cloud.smooth_taubin(
                    iterations=int(iterations),
                    lambda_=float(filter_lambda),
                    mu=float(filter_mu),
                    knn=int(knn),
                    use_fixed_neighborhoods=self.fixed_neighborhoods,
                )

        return parameters, evaluate

    def process(self):
        if not self.inputs["Point Cloud"].is_linked:
            return
        if not self.outputs["Point Cloud"].is_linked:
            return

        point_clouds = self.inputs["Point Cloud"].sv_get(deepcopy=False)
        if isinstance(point_clouds, o3d.geometry.PointCloud):
            point_clouds = [point_clouds]

        parameters, evaluate = self._get_method_data()
        result = _process_geometry_tree(
            point_clouds,
            parameters,
            evaluate,
            list_match_func[self.list_match],
        )
        self.outputs["Point Cloud"].sv_set(result)


def register():
    bpy.utils.register_class(SvO3PointCloudSmoothNode)


def unregister():
    bpy.utils.unregister_class(SvO3PointCloudSmoothNode)
