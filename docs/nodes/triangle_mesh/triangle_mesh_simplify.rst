Triangle Mesh Simplify
======================
Functionality
-------------

Reduces Triangle Mesh complexity using one of three methods.

Input
-----

**O3D Triangle Mesh**
    Source mesh.

Quadric Decimation
~~~~~~~~~~~~~~~~~~

**Triangle Number**
    Target triangle count.

**Boundary Weight**
    Weight used to preserve boundaries.

Vertex Clustering
~~~~~~~~~~~~~~~~~

**Voxel Size**
    Voxel size used to cluster vertices.

**Contraction Method**
    **Average** or **Quadric**.

Merge By Distance
~~~~~~~~~~~~~~~~~

**Distance**
    Vertices closer than this distance are merged. The node subsequently
    removes degenerate and duplicated triangles.

Output
------

**O3D Triangle Mesh**
    Simplified mesh.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.simplify_quadric_decimation <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.simplify_quadric_decimation>`_
* `TriangleMesh.simplify_vertex_clustering <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.simplify_vertex_clustering>`_
* `TriangleMesh.merge_close_vertices <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.merge_close_vertices>`_
* `Open3D mesh tutorial <https://www.open3d.org/docs/latest/tutorial/geometry/mesh.html>`_
