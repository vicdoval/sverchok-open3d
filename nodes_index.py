# struct of menu of addon
def nodes_index():
    return [{"Open 3D": [                                   # Group menu name
                ({'icon_name': 'SV_O3_OPEN3D_LOGO'}, ),     # icon image ID of Group menu name. Used only first elem of tuple
                ("utils.o3d_import", "SvO3ImportNode"),     # Menu item path and class name
                ("utils.o3d_export", "SvO3ExportNode"),
                ("utils.o3d_transform", "SvO3Transform"),
                {"Point Cloud": [
                    ({'icon_name': 'OUTLINER_DATA_POINTCLOUD'}, ),
                    ("point_cloud.point_cloud_in", "SvO3PointCloudInNode"),
                    ("point_cloud.point_cloud_out", "SvO3PointCloudOutNode"),
                    ("point_cloud.point_cloud_downsample", "SvO3PointCloudDownSampleNode"),
                    ("point_cloud.point_cloud_mask", "SvO3PointCloudMaskNode"),
                    ("point_cloud.point_cloud_join", "SvO3PointCloudJoinNode"),
                    ("point_cloud.point_cloud_calc_normals", "SvO3PointCloudCalcNormalsNode"),
                    ]},
                {"Triangle Mesh": [
                    ({'icon_name': 'SV_DELAUNAY'}, ),
                    ("triangle_mesh.triangle_mesh_in", "SvO3TriangleMeshInNode"),
                    ("triangle_mesh.triangle_mesh_out", "SvO3TriangleMeshOutNode"),
                    None,
                    ("triangle_mesh.triangle_mesh_from_point_cloud", "SvO3TriangleMeshFromPointCloudNode"),
                    ("triangle_mesh.triangle_mesh_sampling", "SvO3TriangleMeshSamplingNode"),
                    None,
                    ("triangle_mesh.triangle_mesh_simplify", "SvO3TriangleMeshSimplifyNode"),
                    ("triangle_mesh.triangle_mesh_subdivide", "SvO3TriangleMeshSubdivideNode"),
                    ("triangle_mesh.triangle_mesh_poke", "SvO3TriangleMeshPokeNode"),
                    ("triangle_mesh.triangle_mesh_smooth", "SvO3TriangleMeshSmoothNode"),
                    ("triangle_mesh.triangle_mesh_sharpen", "SvO3TriangleMeshSharpenNode"),
                    ("triangle_mesh.triangle_mesh_deform_as_rigid", "SvO3TriangleMeshDeformAsRigidNode"),
                    None,
                    ("triangle_mesh.triangle_mesh_mask", "SvO3TriangleMeshMaskNode"),
                    ("triangle_mesh.triangle_mesh_separate", "SvO3TriangleMeshSeparateNode"),
                    ("triangle_mesh.triangle_mesh_join", "SvO3TriangleMeshJoinNode"),
                    None,
                    ("triangle_mesh.triangle_mesh_intersect", "SvO3TriangleMeshIntersectNode"),
                    ("triangle_mesh.triangle_mesh_self_intersect", "SvO3TriangleMeshSelfIntersectNode"),
                    ("triangle_mesh.triangle_mesh_clean", "SvO3TriangleMeshCleanNode"),
                ]},
            ]}]
