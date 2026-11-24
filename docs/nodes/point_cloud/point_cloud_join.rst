Point Cloud Join
================
Functionality
-------------

Joins multiple Open3D Point Clouds into a single Point Cloud by concatenating
their points.

Normals and colors are preserved when possible. If only some input Point
Clouds carry an attribute, the node fills missing values so the joined
attribute can match the joined point count.

Input
-----

**O3D Point Cloud**
    List of Point Clouds to join.

Output
------

**O3D Point Cloud**
    Combined Point Cloud.

Nesting
-------

The node joins the Point Clouds at the functional list level. Use Sverchok
list structure to control which groups are joined together.

Open3D Reference
----------------

* `open3d.geometry.PointCloud <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html>`_
