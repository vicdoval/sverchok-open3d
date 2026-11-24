Triangle Mesh Sampling
======================
Functionality
-------------

Samples points on the surface of an Open3D Triangle Mesh and returns an Open3D
Point Cloud.

Inputs
------

**O3D Triangle Mesh**
    Source mesh.

**Points Number**
    Number of points to generate.

**Seed**
    Random seed when supported by the installed Open3D sampling API.

Parameters
----------

**Method**
    **Uniform** samples points uniformly by triangle area.

    **Poisson Disk** produces a more evenly spaced blue-noise distribution.

**Normal**
    **From Faces** uses triangle normals.

    **From Vertex** computes/uses vertex normals.

    **None** does not request triangle-normal sampling.

**Init Factor**
    Poisson Disk only. Controls the size of the initial uniformly sampled
    candidate set.

Output
------

**O3D Point Cloud**
    Sampled Point Cloud.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `TriangleMesh.sample_points_uniformly <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.sample_points_uniformly>`_
* `TriangleMesh.sample_points_poisson_disk <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.sample_points_poisson_disk>`_
