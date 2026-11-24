Triangle Mesh from Point Cloud
==============================
Functionality
-------------

Reconstructs an Open3D Triangle Mesh from a Point Cloud.

Inputs
------

**O3D Point Cloud**
    Source Point Cloud.

Alpha Shape
~~~~~~~~~~~

**Alpha**
    Alpha-shape parameter. Larger values approach the convex hull.

Ball Pivoting
~~~~~~~~~~~~~

**Radius**
    Ball radius used by the reconstruction.

Poisson
~~~~~~~

**Depth**
    Maximum octree depth used by Poisson reconstruction.

**Scale**
    Ratio between the reconstruction cube and the sample bounding cube.

**Density filter**
    Optional minimum density threshold used by the node to remove reconstructed
    vertices.

Parameters
----------

**Method**
    **Alpha Shape**, **Ball Pivoting**, or **Poisson**.

**Processing Threads**
    Poisson thread count. ``-1`` lets Open3D choose automatically.

Normals
-------

Ball Pivoting and Poisson require oriented Point Cloud normals. If the input
Point Cloud does not contain normals, the node asks Open3D to estimate them.

Outputs
-------

**O3D Triangle Mesh**
    Reconstructed mesh.

**Density**
    Poisson density values. This output is relevant to Poisson reconstruction.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.create_from_point_cloud_alpha_shape <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape>`_
* `TriangleMesh.create_from_point_cloud_ball_pivoting <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting>`_
* `TriangleMesh.create_from_point_cloud_poisson <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.create_from_point_cloud_poisson>`_
* `Open3D surface reconstruction tutorial <https://www.open3d.org/docs/latest/tutorial/geometry/surface_reconstruction.html>`_
