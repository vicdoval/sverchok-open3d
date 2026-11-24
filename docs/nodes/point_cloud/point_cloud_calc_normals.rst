Point Cloud Calculate Normals
=============================
Functionality
-------------

Calculates normals for an Open3D Point Cloud and returns both the updated
Point Cloud and the normal vectors.

Inputs
------

**O3D Point Cloud**
    Source Point Cloud.

**Quality**
    Number of nearest neighbors used by Open3D.

Parameters
----------

**Normal Method**
    **Standard** uses Open3D normal estimation.

    **Tangent Plane** additionally orients the estimated normals consistently.

**Output NumPy**
    Outputs the **Normals** data as a NumPy array instead of Python lists.

Outputs
-------

**O3D Point Cloud**
    A copy of the Point Cloud with calculated normals.

**Normals**
    Calculated normal vectors.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `PointCloud.estimate_normals <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.estimate_normals>`_
* `PointCloud.orient_normals_consistent_tangent_plane <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.orient_normals_consistent_tangent_plane>`_
