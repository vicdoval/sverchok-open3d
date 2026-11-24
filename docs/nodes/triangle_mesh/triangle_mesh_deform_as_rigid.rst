Triangle Mesh Deform as Rigid
=============================
Functionality
-------------

Deforms a Triangle Mesh using Open3D's As-Rigid-As-Possible (ARAP)
implementation based on Sorkine and Alexa, *As-Rigid-As-Possible Surface
Modeling* (2007).

Inputs
------

**O3D Triangle Mesh**
    Mesh to deform.

**Pins Index**
    Vertex indices used as positional constraints.

**Pins Position**
    Target positions for the constrained vertices.

**Max Iterations**
    Maximum optimization iterations.

**Smoothed Alpha**
    Regularization trade-off used by the Smoothed energy model.

Parameters
----------

**Energy Mode**
    **Spokes** or **Smoothed**.

Output
------

**O3D Triangle Mesh**
    Deformed mesh.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.deform_as_rigid_as_possible <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.deform_as_rigid_as_possible>`_
* `Open3D mesh deformation tutorial <https://www.open3d.org/docs/latest/tutorial/geometry/mesh_deformation.html>`_
