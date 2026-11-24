Point Cloud Out
===============
Functionality
-------------

Converts Open3D ``PointCloud`` objects into standard Sverchok data.

Open3D Point Clouds are treated as atomic items. Regular and irregular nesting
is preserved, for example::

    [[PointCloud_A, PointCloud_B], PointCloud_C]

becomes::

    [[data_A, data_B], data_C]

Input
-----

**O3D Point Cloud**
    One or more Open3D Point Clouds at any list nesting level.

Parameters
----------

**Output NumPy**
    When disabled, output data leaves are Python lists.

    When enabled, output data leaves are NumPy arrays while the surrounding
    Sverchok list structure is preserved.

    The toggle is available from the extended node properties and directly in
    the node right-click menu.

Outputs
-------

**Vertices**
    Point coordinates, shape ``(N, 3)``.

**Normals**
    Point normals, shape ``(N, 3)``. Empty when the Point Cloud has no normals.

**Colors**
    Point colors converted from Open3D RGB to Sverchok RGBA with alpha ``1.0``,
    shape ``(N, 4)``.

**Nearest Neighbor Distance**
    Nearest-neighbor distance for each point, shape ``(N,)``.

Performance
-----------

Only linked outputs are evaluated. Nearest-neighbor distances are therefore
computed only when that output is connected.

Open3D Reference
----------------

* `open3d.geometry.PointCloud <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html>`_
* `PointCloud.compute_nearest_neighbor_distance <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.compute_nearest_neighbor_distance>`_
* `Open3D - Working with NumPy <https://www.open3d.org/docs/latest/tutorial/geometry/working_with_numpy.html>`_
