Triangle Mesh Subdivide
=======================
Functionality
-------------

Subdivides an Open3D Triangle Mesh.

Inputs
------

**O3D Triangle Mesh**
    Source mesh.

**Iterations**
    Number of subdivision iterations. Each iteration replaces every triangle
    with four triangles.

Parameters
----------

**Method**
    **Loop** uses Loop subdivision and smooths the surface.

    **Midpoint** splits triangles at edge midpoints while preserving the
    original surface.

Output
------

**O3D Triangle Mesh**
    Subdivided mesh.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.subdivide_loop <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.subdivide_loop>`_
* `TriangleMesh.subdivide_midpoint <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.subdivide_midpoint>`_
