from sverchok_open3d.dependencies import open3d as o3d
import numpy as np
def calc_point_cloud_normals(pcd, quality, method):
    s_p = o3d.geometry.KDTreeSearchParamKNN(quality)
    pcd.estimate_normals(search_param=s_p)
    if method == 'TANGENT':
        pcd.orient_normals_consistent_tangent_plane(quality)
