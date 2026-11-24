Triangle Mesh Self Intersect
============================
Functionality
-------------

Checks an Open3D Triangle Mesh for self-intersections and optionally returns
the intersecting triangle pairs.

Input
-----

**O3D Triangle Mesh**
    Mesh to test.

Parameters
----------

**Output NumPy**
    When enabled, **Faces Pairs** is returned as a NumPy array.

Outputs
-------

**Is Self-intersecting**
    Boolean result.

**Faces Pairs**
    Pairs of triangle indices reported by Open3D. Empty when there is no
    self-intersection.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.is_self_intersecting <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.is_self_intersecting>`_
* `TriangleMesh.get_self_intersecting_triangles <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.get_self_intersecting_triangles>`_
