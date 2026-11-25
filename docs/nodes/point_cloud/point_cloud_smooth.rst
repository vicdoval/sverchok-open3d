Point Cloud Smooth
==================

Functionality
-------------

Smooths Open3D ``PointCloud`` geometry using the point-cloud smoothing
algorithms introduced in Open3D 0.20.

The node supports arbitrary and irregular Point Cloud nesting. Sverchok
**List Match** is applied when geometry and numerical parameters reach their
functional levels.

Input
-----

**Point Cloud**
    One or more Open3D Point Clouds.

Methods
-------

MLS
~~~

Moving Least Squares style smoothing. Open3D fits a weighted local tangent
plane and projects each point onto it.

**Radius**
    Hybrid-search radius.

**Max Neighbors**
    Maximum number of neighbors used by the hybrid search.

Bilateral
~~~~~~~~~

Feature-preserving bilateral smoothing using spatial and normal-direction
weights. Open3D estimates normals internally if they are missing.

**Radius**
    Hybrid-search radius.

**Max Neighbors**
    Maximum neighbors used by the hybrid search.

**Sigma Spatial**
    Spatial Gaussian standard deviation.

**Sigma Range**
    Range Gaussian standard deviation along the local normal direction.

Laplacian
~~~~~~~~~

Laplacian smoothing on a K-nearest-neighbor graph.

**Iterations**
    Number of smoothing iterations.

**Lambda**
    Laplacian smoothing factor.

**KNN**
    Number of nearest neighbors.

**Fixed Neighborhoods**
    Reuses the initial KNN graph across iterations. This can improve
    performance, but may reduce quality for large deformations.

Taubin
~~~~~~

Alternating Laplacian and inverse-Laplacian passes to reduce shrinkage.

**Iterations**
    Number of smoothing iterations.

**Lambda**
    Positive Laplacian smoothing factor.

**Mu**
    Inverse-Laplacian factor. Open3D defaults to ``-0.53``.

**KNN**
    Number of nearest neighbors.

**Fixed Neighborhoods**
    Reuses the initial KNN graph across iterations.

Output
------

**Point Cloud**
    Smoothed Open3D Point Cloud.

List Matching and Nesting
-------------------------

The node preserves geometry nesting. For example::

    [A]

returns::

    [smooth(A)]

and::

    [[A, B], C]

returns::

    [[smooth(A), smooth(B)], smooth(C)]

Numerical socket wrappers do not add an extra Point Cloud nesting level.

The **List Match** option controls how geometry and numerical parameter lists
of different lengths are paired.

Requirements
------------

Point Cloud smoothing requires Open3D 0.20 or newer.

Open3D Reference
----------------

* `PointCloud.smooth_mls <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.smooth_mls>`_
* `PointCloud.smooth_bilateral <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.smooth_bilateral>`_
* `PointCloud.smooth_laplacian <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.smooth_laplacian>`_
* `PointCloud.smooth_taubin <https://www.open3d.org/docs/latest/python_api/open3d.geometry.PointCloud.html#open3d.geometry.PointCloud.smooth_taubin>`_
* `Open3D 0.20 release notes <https://www.open3d.org/2026/09/24/open3d-v0-20-is-here-with-gaussian-splatting-and-full-intel-gpu-support/>`_
