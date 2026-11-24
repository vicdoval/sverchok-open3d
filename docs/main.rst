Sverchok-Open3D
================

Sverchok-Open3D exposes Open3D geometry and processing operations as Sverchok
nodes. The addon currently works with Open3D legacy ``PointCloud`` and
``TriangleMesh`` geometry objects.

The pages below describe the Sverchok-facing behavior of each node and link to
the corresponding Open3D API documentation.

.. toctree::
   :maxdepth: 2
   :caption: Utilities

   nodes/utils/o3d_import
   nodes/utils/o3d_export
   nodes/utils/o3d_transform

.. toctree::
   :maxdepth: 2
   :caption: Point Cloud

   nodes/point_cloud/point_cloud_in
   nodes/point_cloud/point_cloud_out
   nodes/point_cloud/point_cloud_downsample
   nodes/point_cloud/point_cloud_mask
   nodes/point_cloud/point_cloud_join
   nodes/point_cloud/point_cloud_calc_normals
   nodes/point_cloud/point_cloud_outlier_removal

.. toctree::
   :maxdepth: 2
   :caption: Triangle Mesh

   nodes/triangle_mesh/triangle_mesh_in
   nodes/triangle_mesh/triangle_mesh_out
   nodes/triangle_mesh/triangle_mesh_from_point_cloud
   nodes/triangle_mesh/triangle_mesh_sampling
   nodes/triangle_mesh/triangle_mesh_simplify
   nodes/triangle_mesh/triangle_mesh_subdivide
   nodes/triangle_mesh/triangle_mesh_poke
   nodes/triangle_mesh/triangle_mesh_smooth
   nodes/triangle_mesh/triangle_mesh_sharpen
   nodes/triangle_mesh/triangle_mesh_deform_as_rigid
   nodes/triangle_mesh/triangle_mesh_mask
   nodes/triangle_mesh/triangle_mesh_separate
   nodes/triangle_mesh/triangle_mesh_join
   nodes/triangle_mesh/triangle_mesh_intersect
   nodes/triangle_mesh/triangle_mesh_self_intersect
   nodes/triangle_mesh/triangle_mesh_clean

Open3D
------

The upstream Open3D documentation is available at
`open3d.org/docs/latest <https://www.open3d.org/docs/latest/>`_.
