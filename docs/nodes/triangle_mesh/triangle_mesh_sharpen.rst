Triangle Mesh Sharpen
=====================
Functionality
-------------

Sharpens an Open3D Triangle Mesh using Open3D's mesh sharpening filter.

Inputs
------

**O3D Triangle Mesh**
    Source mesh.

**Iterations**
    Number of sharpening iterations.

**Strength**
    Sharpening strength.

Output
------

**O3D Triangle Mesh**
    Sharpened mesh.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.filter_sharpen <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.filter_sharpen>`_
