Open3D Export
=============
Functionality
-------------

Writes Open3D Point Clouds or Triangle Meshes to disk. Export is executed when
the **EXPORT** button is pressed.

Inputs
------

**Folder Path**
    Destination folder.

**O3D Point Cloud**
    Point Clouds to export when **Export** is set to **Point Cloud**.

**O3D Triangle Mesh**
    Triangle Meshes to export when **Export** is set to **Triangle Mesh**.

Parameters
----------

**Export**
    Selects Point Cloud or Triangle Mesh output.

**Base Name**
    Base file name. Objects are numbered sequentially.

**Write Ascii**
    Writes ASCII where supported by the selected Open3D writer.

**Compressed**
    Requests compressed output where supported.

**Print Progress in console**
    Displays Open3D export progress.

Triangle Mesh only:

**Write Vertex Normals**
    Include vertex normals when available.

**Write Vertex Colors**
    Include vertex colors when available.

**Write Triangle UVs**
    Include triangle UV coordinates when available.

Output Formats
--------------

The current node writes Point Clouds as ``.ply`` and Triangle Meshes as
``.obj``.

Open3D Reference
----------------

* `open3d.io.write_point_cloud <https://www.open3d.org/docs/latest/python_api/open3d.io.write_point_cloud.html>`_
* `open3d.io.write_triangle_mesh <https://www.open3d.org/docs/latest/python_api/open3d.io.write_triangle_mesh.html>`_
