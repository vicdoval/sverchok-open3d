Triangle Mesh Out
=================
Functionality
-------------

Converts Open3D ``TriangleMesh`` objects into Sverchok mesh and attribute data.

Open3D meshes are treated as atomic items. Regular and irregular nesting is
preserved exactly.

Input
-----

**O3D Triangle Mesh**
    One or more Open3D Triangle Mesh objects at any list nesting level.

Parameters
----------

**Output NumPy**
    NumPy output can be enabled independently for every output.

    The right-click menu contains an **Output NumPy** submenu with one toggle
    per output socket. The same controls are also available in the extended
    node properties.

Outputs
-------

**Vertices**
    Vertex coordinates, shape ``(N, 3)``.

**Edges**
    Unique edges derived from the triangles, shape ``(E, 2)``.

**Faces**
    Triangle indices, shape ``(F, 3)``.

**Vertex Normal**
    Vertex normals. Missing normals are calculated when this output is linked.

**Vertex Color**
    Open3D RGB colors converted to RGBA.

**Face Normal**
    Triangle normals. Missing normals are calculated when this output is linked.

**Face Center**
    Triangle centers.

**Face Area**
    Triangle areas.

**UV Verts**
    Open3D triangle UV coordinates converted to 3D Sverchok UV vertices
    (``Z = 0``).

**UV Faces**
    Triangle indices for **UV Verts**.

**Material Id**
    Triangle material IDs.

Performance
-----------

Only linked outputs are calculated.

Open3D Reference
----------------

* `open3d.geometry.TriangleMesh <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html>`_
* `Open3D - Working with NumPy <https://www.open3d.org/docs/latest/tutorial/geometry/working_with_numpy.html>`_
