import numpy as np
import copy
import bpy
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode
from sverchok_open3d.dependencies import open3d as o3d

class SvO3PointCloudJoinNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
    """
    Triggers: O3D Point Cloud Join
    Tooltip: Open3D  Point Cloud Join
    """
    bl_idname = 'SvO3PointCloudJoinNode'
    bl_label = 'Point Cloud Join'
    bl_icon = 'OUTLINER_OB_POINTCLOUD'
    sv_icon = 'SV_RANDOM_NUM_GEN'
    sv_dependencies = ['open3d']

    def sv_init(self, context):
        self.width = 150
        pcd = self.inputs.new('SvO3PointCloudSocket', "O3D Point Cloud")
        pcd.is_mandatory = True
        pcd.nesting_level = 1
        self.outputs.new('SvO3PointCloudSocket', "O3D Point Cloud")

    def process_data(self, params):
        pcd_in = params[0]
        new_pcd = copy.deepcopy(pcd_in[0])
        new_pcd.points = o3d.utility.Vector3dVector(
            np.concatenate([np.asarray(pcd.points) for pcd in pcd_in])
            )

        has_normals = [pcd.has_normals() for pcd in pcd_in]
        if all(has_normals):
            new_pcd.normals = o3d.utility.Vector3dVector(
                np.concatenate([np.asarray(pcd.normals)  for pcd in pcd_in])
                )
        elif any(has_normals):
            new_pcd.normals = o3d.utility.Vector3dVector(
                np.concatenate([np.asarray(pcd.normals) if pcd.has_normals() else np.zeros((len(pcd.points), 3), dtype='float')  for pcd in pcd_in])
                )


        has_colors = [pcd.has_colors() for pcd in pcd_in]
        if all(has_colors):
            new_pcd.colors = o3d.utility.Vector3dVector(
                np.concatenate([np.asarray(pcd.colors)  for pcd in pcd_in])
                )
        elif any(has_colors):
            new_pcd.colors = o3d.utility.Vector3dVector(
                np.concatenate([np.asarray(pcd.colors) if pcd.has_colors else np.zeros((len(pcd.colors), 3), dtype='float')
                                for pcd in pcd_in])
                )


        return [new_pcd]



def register():
    bpy.utils.register_class(SvO3PointCloudJoinNode)

def unregister():
    bpy.utils.unregister_class(SvO3PointCloudJoinNode)
