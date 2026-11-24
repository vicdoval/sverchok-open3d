Open3D Transform
================
Functionality
-------------

Transforms Open3D Point Clouds or Triangle Meshes while keeping the result as
Open3D geometry.

The transformation input type determines the operating mode:

* Matrix
* Vector list
* Vector Field
* Number list
* Scalar Field

Matrix, vector-list and vector-field transformations work with Point Clouds
and Triangle Meshes. Number and Scalar Field inputs displace Triangle Mesh
vertices along mesh normals.

Inputs
------

**O3D Geometry**
    Open3D Point Cloud or Triangle Mesh.

**Transformation**
    Matrix, vector list, Vector Field, number list or Scalar Field.

**Mask**
    Optional point/vertex mask.

**Iterations**
    Number of repeated transformation steps.

**Coefficient**
    Multiplier applied at each iteration. A list of coefficients is cycled
    across iterations.

Output
------

**O3D Geometry**
    A transformed copy of the input geometry. The output socket adapts to the
    input Open3D geometry type.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `Open3D transformation tutorial <https://www.open3d.org/docs/latest/tutorial/geometry/transformation.html>`_
* `open3d.geometry.PointCloud <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html>`_
* `open3d.geometry.TriangleMesh <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html>`_
