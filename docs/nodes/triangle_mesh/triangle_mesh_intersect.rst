Triangle Mesh Intersects
========================
Functionality
-------------

Tests whether pairs of Open3D Triangle Meshes intersect.

Inputs
------

**O3D Triangle Mesh A**
    First mesh.

**O3D Triangle Mesh B**
    Second mesh.

Output
------

**Intersect**
    Boolean result for each matched mesh pair.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.is_intersecting <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.is_intersecting>`_
