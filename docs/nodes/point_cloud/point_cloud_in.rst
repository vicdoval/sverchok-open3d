Point Cloud In
==============
Functionality
-------------

Creates Open3D ``PointCloud`` objects from Sverchok vertex, normal and color
data.

Inputs
------

**Vertices**
    Point coordinates. Required.

**Normals**
    Optional point normals.

**Colors**
    Optional RGB or RGBA colors. Only RGB is stored by Open3D.

Parameters
----------

When **Normals** is not connected:

**Normal Method**
    **Standard** estimates normals from neighboring points.

    **Tangent Plane** estimates normals and then orients them consistently
    using tangent-plane propagation.

    **None** creates the Point Cloud without normals.

**Normal Quality**
    Number of nearest neighbors used by the normal estimation/orientation
    routines.

Output
------

**O3D Point Cloud**
    Open3D Point Cloud containing the supplied data.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `open3d.geometry.PointCloud <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html>`_
* `PointCloud.estimate_normals <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.estimate_normals>`_
* `PointCloud.orient_normals_consistent_tangent_plane <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.orient_normals_consistent_tangent_plane>`_
