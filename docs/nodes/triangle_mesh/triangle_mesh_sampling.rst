Triangle Mesh Sampling
======================

Functionality
-------------

Points over Open3d Triangle mesh. Mesh to Point Cloud

Inputs
------

*O3D Triangle Mesh*
*Points Number*
*Seed*


Parameters
----------
*Method*:
  "Uniform": Uniform Sampling
  "Poisson Disk: Poisson Disk Sampling

*Normal Methods*:
  *From Faces*: Calculate Normals From Faces.
  *From Vertex*: Calculate Normals From Vertices.
  *None*: If mesh does not carry Normals, the point cloud will not have Normals.




Output
------

*O3D Point Cloud*


Examples
--------
