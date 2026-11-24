Triangle Mesh In
================
Functionality
-------------

Creates or updates an Open3D ``TriangleMesh`` from Sverchok mesh data.

The node can either build a new Triangle Mesh or use an existing Open3D
Triangle Mesh as a base and replace connected attributes.

Inputs
------

**O3D Triangle Mesh**
    Optional base mesh.

**Vertices**
    Vertex coordinates.

**Vertex Normals**
    Optional vertex normals.

**Vertex Colors**
    Optional RGB/RGBA colors. Open3D stores RGB.

**Faces**
    Triangle indices. Only triangular faces are accepted.

**Face Normals**
    Optional triangle normals.

**UV Verts**
    UV coordinates supplied as Sverchok vertices.

**UV Faces**
    Indices mapping the UV vertices to triangles.

**Material Id**
    Triangle material IDs.

Output
------

**O3D Triangle Mesh**
    Resulting Open3D Triangle Mesh.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `open3d.geometry.TriangleMesh <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html>`_
* `Open3D - Working with NumPy <https://www.open3d.org/docs/latest/tutorial/geometry/working_with_numpy.html>`_
