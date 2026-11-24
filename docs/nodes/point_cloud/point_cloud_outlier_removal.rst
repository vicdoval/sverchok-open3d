Point Cloud Outlier Removal
===========================
Functionality
-------------

Removes sparse or statistically anomalous points from Open3D Point Clouds.

The node supports arbitrary Point Cloud nesting and applies Sverchok list
matching to the numerical parameters at the functional data level.

Input
-----

**O3D Point Cloud**
    Source Point Cloud.

Method: Statistical
~~~~~~~~~~~~~~~~~~~

**Neighbors**
    Number of neighbors used to estimate the mean distance around each point.

**Std Ratio**
    Standard-deviation threshold. Smaller values generally remove more points.

Method: Radius
~~~~~~~~~~~~~~

**Points**
    Minimum number of neighboring points required inside the radius.

**Radius**
    Neighborhood radius.

Parameters
----------

**Method**
    **Statistical** or **Radius**.

**List Match**
    Controls matching when Point Cloud and parameter lists have different
    lengths.

Outputs
-------

**Point Cloud**
    Inlier Point Cloud.

**Outliers**
    Removed points.

**Indices**
    Indices of the retained points in the original Point Cloud.

**Mask**
    Boolean mask aligned with the original points. ``True`` means the point was
    retained.

Open3D Reference
----------------

* `PointCloud.remove_statistical_outlier <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.remove_statistical_outlier>`_
* `PointCloud.remove_radius_outlier <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.remove_radius_outlier>`_
* `Open3D point cloud outlier removal tutorial <https://www.open3d.org/docs/latest/tutorial/geometry/pointcloud_outlier_removal.html>`_
