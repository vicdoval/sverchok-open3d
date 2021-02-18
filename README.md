SVERCHOK OPEN3D
===============

This is an addon for [Blender][1], was that extends [Sverchok][2]
addon. Bringing functionalities from the [Open 3d][7] library.

**NOTE**: Sverchok-Open3d contains nodes that may crash Blender so please save frequently.


The documentation is absent, but you can check the open3d documentation.

Features
--------

At the moment, this addon includes the following nodes for Sverchok:

* *Point Cloud In*: create Point Cloud from Sverchok Data
* *Point Cloud Out*: Point Cloud to Sverchok Data
* *Point Cloud Import*: Import Point Cloud form file
* *Point Cloud Export*: Export Point Cloud to file
* *Mesh from Point Cloud*: Creates mesh from Point Cloud, offers Alpha Shape, Ball Pivoting and Poisson Reconstruction algorithms

There will be more.

Installation
------------

* Download and Install [Sverchok][2]
* Download [Sverchok-Open3d zip archive][4] from GitHub
* In Blender, go to User Preferences > Addons > install from file > choose
  zip-archive > activate flag beside Sverchok-Open3d.
* In the addon options you will see if you have already installed Open3d library otherwise click on "Install with Pip"
* Save preferences, if you want to enable the addon permanently.

LICENSE: GPL-3.

[1]: http://blender.org
[2]: https://github.com/nortikin/sverchok
[4]: https://github.com/vicdoval/sverchok-open3d/archive/master.zip
[6]: https://github.com/nortikin/sverchok/wiki/Dependencies
[7]: http://www.open3d.org/
