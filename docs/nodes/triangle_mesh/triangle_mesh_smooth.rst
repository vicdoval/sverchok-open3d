Triangle Mesh Smooth
====================
Functionality
-------------

Smooths an Open3D Triangle Mesh.

Inputs
------

**O3D Triangle Mesh**
    Source mesh.

**Iterations**
    Number of smoothing iterations.

**Lambda**
    Reserved smoothing parameter input.

**Mu**
    Reserved Taubin smoothing parameter input.

Parameters
----------

**Method**
    **Simple**, **Laplacian**, or **Taubin**.

Output
------

**O3D Triangle Mesh**
    Smoothed mesh.

Notes
-----

The current node exposes Lambda and Mu sockets, but its Open3D calls use the
Open3D default values for those parameters.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.filter_smooth_simple <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.filter_smooth_simple>`_
* `TriangleMesh.filter_smooth_laplacian <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.filter_smooth_laplacian>`_
* `TriangleMesh.filter_smooth_taubin <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.filter_smooth_taubin>`_
