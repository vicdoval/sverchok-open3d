Triangle Mesh Poke
==================
Functionality
-------------

Pokes selected triangles by inserting a new vertex at each selected triangle
center and replacing that triangle with three new triangles.

This is a Sverchok-Open3D operation built on top of the Open3D
``TriangleMesh`` data model rather than a single Open3D API method.

Inputs
------

**O3D Triangle Mesh**
    Source mesh.

**Offset**
    Moves each new center vertex along the triangle normal.

**Mask**
    Selects triangles to poke.

**New Vertex Color**
    Optional color for the inserted vertices.

**New Material Id**
    Optional material ID for the generated triangles.

Parameters
----------

**Relative Offset**
    Multiplies the offset by the selected triangle area.

**Output NumPy**
    Available in extended properties for the auxiliary outputs.

Outputs
-------

**O3D Triangle Mesh**
    Poked mesh.

**New Vertices**
    Coordinates of inserted vertices.

**New Verts Idx**
    Indices of inserted vertices.

**New Faces Idx**
    Indices of generated faces.

Attribute Handling
------------------

The node attempts to propagate existing vertex colors, vertex normals,
triangle normals, triangle UVs and material IDs to the generated topology.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `open3d.geometry.TriangleMesh <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html>`_
