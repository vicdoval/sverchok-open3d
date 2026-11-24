Triangle Mesh Mask
==================
Functionality
-------------

Removes selected vertices or triangles from an Open3D Triangle Mesh.

Inputs
------

**O3D Triangle Mesh**
    Source mesh.

**Index**
    Indices used in **Index** filter mode.

**Mask**
    Boolean mask used in **Mask** filter mode.

Parameters
----------

**Method**
    **Verts** removes vertices.

    **Triangles** removes triangles.

**Filter Method**
    **Index** or **Mask**.

**Invert**
    Inverts which elements are removed.

**Remove Unreferenced Vertices**
    Available in Triangle mode. Removes vertices left unused after triangle
    removal.

Output
------

**O3D Triangle Mesh**
    Filtered mesh.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.remove_vertices_by_mask <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.remove_vertices_by_mask>`_
* `TriangleMesh.remove_triangles_by_mask <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.remove_triangles_by_mask>`_
* `TriangleMesh.remove_unreferenced_vertices <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.remove_unreferenced_vertices>`_
