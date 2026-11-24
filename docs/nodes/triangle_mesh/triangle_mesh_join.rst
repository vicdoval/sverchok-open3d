Triangle Mesh Join
==================
Functionality
-------------

Joins multiple Open3D Triangle Meshes into a single Triangle Mesh by
concatenating vertices and remapping triangle indices.

Input
-----

**O3D Triangle Mesh**
    Meshes to join.

Parameters
----------

**Compute Vertex Normals**
    Computes vertex normals when they cannot be preserved directly.

**Compute Faces Normals**
    Computes triangle normals when they cannot be preserved directly.

Output
------

**O3D Triangle Mesh**
    Combined mesh.

Attributes
----------

The node attempts to preserve vertex colors, triangle UVs and triangle
material IDs when present.

Open3D Reference
----------------

* `open3d.geometry.TriangleMesh <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html>`_
* `TriangleMesh.compute_vertex_normals <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.compute_vertex_normals>`_
* `TriangleMesh.compute_triangle_normals <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.compute_triangle_normals>`_
