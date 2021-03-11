
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.logging import info, exception
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

import numpy as np
from sverchok_open3d.dependencies import open3d as o3d
from sverchok.utils.dummy_nodes import add_dummy

if o3d is None:
    add_dummy('SvO3PointCloudMaskNode', 'Point Cloud Mask', 'open3d')
else:
    class SvO3PointCloudMaskNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: O3D Point Cloud Mask
        Tooltip: Point Cloud Mask
        """
        bl_idname = 'SvO3PointCloudMaskNode'
        bl_label = 'Point Cloud Mask'
        bl_icon = 'OUTLINER_OB_POINTCLOUD'
        sv_icon = 'SV_RANDOM_NUM_GEN'

        filter_methods = [
            ('INDEX', "Index", "Index", 0),
            ('MASK', "Mask", "Mask", 1),
        ]
        def update_sockets(self, context):
            self.inputs['Index'].hide_safe = self.filter_method != 'INDEX'
            self.inputs['Mask'].hide_safe = self.filter_method != 'MASK'
            updateNode(self, context)

        filter_method: EnumProperty(
            name="Filter Method",
            items=filter_methods,
            default='INDEX',
            update=update_sockets)

        index: IntProperty(
            name="Index",
            default=0,
            update=updateNode)

        def sv_init(self, context):
            self.inputs.new('SvO3PointCloudSocket', 'O3D Point Cloud').is_mandatory = True
            self.inputs.new('SvStringsSocket', "Index").prop_name = 'index'
            self.inputs.new('SvStringsSocket', "Mask").hide_safe = True

            self.outputs.new('SvO3PointCloudSocket', "O3D Point Cloud")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'filter_method')

        def process_data(self, params):

            pcd_out = []

            for pcd, indexes, mask in zip(*params):

                if self.filter_method == 'INDEX':
                    new_pcd = pcd.select_by_index(indexes)
                else:
                    index_n = np.arange(len(pcd.points), dtype='int')[mask]
                    new_pcd = pcd.select_by_index(index_n)


                pcd_out.append(new_pcd)


            return pcd_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3PointCloudMaskNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3PointCloudMaskNode)
