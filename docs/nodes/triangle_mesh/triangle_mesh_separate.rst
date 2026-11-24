Triangle Mesh Separate Loose
============================
Functionality
-------------

Separates a Triangle Mesh into edge-connected triangle clusters.

Input
-----

**O3D Triangle Mesh**
    Source mesh.

Parameters
----------

**Flat List**
    When enabled, all resulting meshes are flattened into one list.

    When disabled, separated parts remain grouped by source mesh.

Outputs
-------

**O3D Triangle Mesh**
    Separated connected components.

**Num of Triangles**
    Triangle count for each connected component.

**Area**
    Surface area for each connected component.

Open3D Reference
----------------

* `TriangleMesh.cluster_connected_triangles <https://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.cluster_connected_triangles>`_
