SVERCHOK OPEN3D
===============

This is an addon for [Blender][1], that extends [Sverchok][2]
addon. Bringing functionalities from the [Open 3d][7] library.

**NOTE**: Sverchok-Open3d contains nodes that may crash Blender so please save frequently.

The documentation is almost absent, but you can check the open3d documentation.

Features
--------

At the moment, this addon includes the following nodes for Sverchok:

* *Open 3d Import*: Import Point Cloud or Triangle mesh form file
* *Open 3d Export*: Export Point Cloud or Triangle mesh form file
* *Open 3d Transform*: Apply transformations to Triangle Mesh or Point Cloud. Accepts Matrix, Vector Field, and Vector Lists to displace vertices/points and Scalar Field and Number List to displace along Normal

* *Point Cloud In*: create Point Cloud from Sverchok Data
* *Point Cloud Out*: Point Cloud to Sverchok Data
* *Point Cloud Downsample*: Reduce density of Point Cloud
* *Point Cloud Mask*: Filter parts of a point cloud
* *Point Cloud Calc Normals*: Calculate Point Cloud normals, offers 'Standard' and 'Tangent Plane' methods

* *Triangle Mesh In*: create Triangle Mesh from Sverchok Data
* *Triangle Mesh Out*: create Triangle Mesh to Sverchok Data
* *Triangle Mesh from Point Cloud*: Creates mesh from Point Cloud, offers Alpha Shape, Ball Pivoting and Poisson Reconstruction algorithms
* *Triangle Mesh Sampling*: Creates Point Cloud from mesh, offers Standard and Poisson Distribution
* *Triangle Mesh Simplify*: Simplifies mesh. Offers: Quadric Decimation, Vertex Clustering and Merge by Distance
* *Triangle Mesh Clean*: Remove doubled faces and verts, align and normalize normals, delete unused verts, Remove non-manifold edges
* *Triangle Mesh Smooth*: Offers Simple, Laplacian and  Taubin algorithms.
* *Triangle Mesh Sharpen*: Sharpen mesh
* *Triangle Mesh Subdivide*: Offers, Loop and Midpoint algorithms.
* *Triangle Mesh Mask*: Filter parts of a Triangle Mesh.
* *Triangle Mesh Separate Loose Parts*: Split separated mesh parts into different meshes.
* *Triangle Mesh Join*: Join multiple meshes into one mesh.
* *Triangle Mesh Mask*: Filter parts of a Triangle Mesh.
* *Triangle Mesh Deform as Rigid*: Deforms the mesh using the method by Sorkine and Alexa, ‘As-Rigid-As-Possible Surface Modeling’, 2007.
* *Triangle Mesh Intersects*: Determine if two meshes intersect.
* *Triangle Mesh Self Intersect*: Determine if one mesh intersect with itself and the intersecting face pairs.


There will be more.

Installation
------------

* Download and Install [Sverchok][2]
* Download [Sverchok-Open3d zip archive][4] from GitHub
* In Blender, go to User Preferences > Addons > install from file > choose
  zip-archive > activate flag beside Sverchok-Open3d.
* In the addon options you will see if you have already installed Open3d library otherwise click on "Install with Pip"
* Save preferences, if you want to enable the addon permanently.

Sverchok Addon Template
-----------------------
The other purpose of this add-on is to serve as template to create external Sverchok Add-ons.
Using this repository as template you will have:
* Your own sockets
* Separators in the Add menu
* Sub menus in the added menus
* Link to your own node documentation from Blender UI
* Examples added to the Sverchok Examples menu
* Update your addon from Blender UI

If there is something you don0nt understand in the code please open a issue so I can add more documentation to the code

LICENSE: GPL-3.

[1]: http://blender.org
[2]: https://github.com/nortikin/sverchok
[4]: https://github.com/vicdoval/sverchok-open3d/archive/master.zip
[6]: https://github.com/nortikin/sverchok/wiki/Dependencies
[7]: http://www.open3d.org/