Point Cloud Downsample
======================
Functionality
-------------

Reduces Point Cloud density using one of three Open3D downsampling methods.

Input
-----

**O3D Point Cloud**
    Point Cloud to downsample.

Method: Uniform
~~~~~~~~~~~~~~~

**Every N**
    Keeps every N-th point.

Method: Voxel
~~~~~~~~~~~~~

**Voxel Size**
    Voxel edge length. Points inside the same voxel are combined by Open3D.

Method: Voxel and Trace
~~~~~~~~~~~~~~~~~~~~~~~

**Voxel Size**
    Voxel edge length.

**Bounding Box**
    Points defining the minimum and maximum bounds used by Open3D.

Parameters
----------

**Method**
    **Uniform**, **Voxel**, or **Voxel and Trace**.

**Approximate Class**
    Advanced Open3D option used by **Voxel and Trace**.

Outputs
-------

**O3D Point Cloud**
    Downsampled Point Cloud.

**Index**
    Visible in **Voxel and Trace** mode. Contains the Open3D trace/index data
    relating output voxels to source points.

List Matching
-------------

The node supports Sverchok list matching. The matching mode is available in
the extended node properties or from the right-click menu. Matching is applied
to the corresponding geometry and parameter lists before the Open3D operation
is evaluated.

Open3D Reference
----------------

* `PointCloud.uniform_down_sample <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.uniform_down_sample>`_
* `PointCloud.voxel_down_sample <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.voxel_down_sample>`_
* `PointCloud.voxel_down_sample_and_trace <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.voxel_down_sample_and_trace>`_
