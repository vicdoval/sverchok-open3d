Open3D Import
=============
Functionality
-------------

Reads a Point Cloud or Triangle Mesh from disk using Open3D.

Input
-----

**File Path**
    One or more file paths. The node reads every path provided by the input.

Parameters
----------

**Import**
    Selects **Point Cloud** or **Triangle Mesh**.

For Point Clouds:

**Remove NaN points**
    Removes points containing NaN coordinates while reading.

**Remove Infinite points**
    Removes points containing infinite coordinates while reading.

For Triangle Meshes:

**Enable Postprocessing**
    Enables Open3D import post-processing.

For both modes:

**Print Progress in console**
    Requests Open3D to print import progress.

Outputs
-------

**O3D Point Cloud**
    Visible when importing Point Clouds.

**O3D Triangle Mesh**
    Visible when importing Triangle Meshes.

Open3D Reference
----------------

* `open3d.io.read_point_cloud <https://www.open3d.org/docs/latest/python_api/open3d.io.read_point_cloud.html>`_
* `open3d.io.read_triangle_mesh <https://www.open3d.org/docs/latest/python_api/open3d.io.read_triangle_mesh.html>`_
