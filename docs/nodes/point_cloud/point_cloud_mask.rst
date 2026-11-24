Point Cloud Mask
================
Functionality
-------------

Selects a subset of an Open3D Point Cloud by explicit point indices or by a
boolean mask.

Inputs
------

**O3D Point Cloud**
    Source Point Cloud.

**Index**
    Point indices to keep when **Filter Method** is **Index**.

**Mask**
    Boolean point mask when **Filter Method** is **Mask**.

Parameters
----------

**Filter Method**
    **Index** or **Mask**.

Output
------

**O3D Point Cloud**
    Point Cloud containing the selected points. Open3D point attributes such
    as normals and colors follow the selected points.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `PointCloud.select_by_index <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.select_by_index>`_
