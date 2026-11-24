Triangle Mesh Clean
===================
Functionality
-------------

Applies selected Open3D mesh cleanup operations to a copy of the input
Triangle Mesh.

Input
-----

**O3D Triangle Mesh**
    Source mesh.

Parameters
----------

**Normalize Normals**
    Normalizes mesh normals.

**Orient Triangles**
    Attempts to orient connected triangles consistently.

Remove options:

**Non Manifold Edges**
    Removes non-manifold edges according to Open3D.

**Duplicated Verts**
    Removes duplicated vertices.

**Degenrated Verts**
    Removes degenerate triangles. The UI label is historical; the operation
    acts on triangles.

**Duplicated Triangles**
    Removes duplicated triangles. Sverchok-Open3D currently uses its own
    duplicate-face cleanup implementation for this option.

**Unreferenced Vertices**
    Removes vertices not referenced by triangles.

Output
------

**O3D Triangle Mesh**
    Cleaned mesh.

Open3D Reference
----------------

* `TriangleMesh.normalize_normals <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.normalize_normals>`_
* `TriangleMesh.orient_triangles <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.orient_triangles>`_
* `TriangleMesh.remove_non_manifold_edges <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.remove_non_manifold_edges>`_
* `TriangleMesh.remove_duplicated_vertices <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.remove_duplicated_vertices>`_
* `TriangleMesh.remove_degenerate_triangles <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.remove_degenerate_triangles>`_
* `TriangleMesh.remove_duplicated_triangles <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.remove_duplicated_triangles>`_
* `TriangleMesh.remove_unreferenced_vertices <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.remove_unreferenced_vertices>`_
