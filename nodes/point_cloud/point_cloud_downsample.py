
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.sv_logging import sv_logger
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

from sverchok_open3d.dependencies import open3d as o3d

if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3PointCloudOutNode', 'Point Cloud Out', 'open3d')
else:
    class SvO3PointCloudDownSampleNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Point Cloud Out
        Tooltip: Point Cloud Out
        """
        bl_idname = 'SvO3PointCloudDownSampleNode'
        bl_label = 'Point Cloud Downsample'
        bl_icon = 'OUTLINER_OB_POINTCLOUD'
        sv_icon = 'SV_RANDOM_NUM_GEN'
        methods = [
            ('UNIFORM', "Uniform", "Uniform", 0),
            ('VOXEL', "Voxel", "Voxel", 1),
            ('VOXEL_AND_TRACE', "Voxel and Trace", "Voxel and Trace", 2),
        ]
        def update_sockets(self, context):
            self.inputs["Every N"].hide_safe = self.method != 'UNIFORM'
            self.inputs["Voxel Size"].hide_safe = self.method == 'UNIFORM'
            self.inputs["Bounding Box"].hide_safe = self.method != 'VOXEL_AND_TRACE'
            self.outputs["Index"].hide_safe = self.method != 'VOXEL_AND_TRACE'
            updateNode(self, context)
        method: EnumProperty(
            name="Method",
            items=methods,
            default='UNIFORM',
            update=update_sockets)
        every_nth: IntProperty(
            name="Every Nth.",
            default=2,
            update=updateNode)
        voxel_size: FloatProperty(
            name="Voxel Size",
            default=0.5,
            update=updateNode)
        approximate_class: BoolProperty(
            name="Approximate_class",
            default=False,
            update=updateNode)

        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3PointCloudSocket', 'O3D Point Cloud').is_mandatory = True
            every_n =  self.inputs.new('SvStringsSocket', "Every N")
            every_n.prop_name = 'every_nth'
            every_n.nesting_level = 1
            every_n.pre_processing = 'ONE_ITEM'
            voxel_size = self.inputs.new('SvStringsSocket', "Voxel Size")
            voxel_size.prop_name = 'voxel_size'
            voxel_size.nesting_level = 1
            voxel_size.pre_processing = 'ONE_ITEM'
            voxel_size.hide_safe = True
            bbox = self.inputs.new('SvVerticesSocket', "Bounding Box")
            bbox.nesting_level = 3
            bbox.hide_safe = True


            self.outputs.new('SvO3PointCloudSocket', 'O3D Point Cloud')
            self.outputs.new('SvStringsSocket', "Index")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'method')

        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')
            layout.prop(self, 'method')
            layout.prop(self, 'approximate_class')

        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")

        def process_data(self, params):

            pcd_out, index_out = [], []
            for pcd, nth, voxel_size, bbox in zip(*params):
                if self.method == 'UNIFORM':
                    new_pcd = pcd.uniform_down_sample(nth)
                elif self.method == 'VOXEL':
                    new_pcd = pcd.voxel_down_sample(voxel_size)
                else:
                    np_bbox = np.array(bbox)
                    if len(bbox) <2:
                        raise  Exception('No valid bounding box given')
                    min_bound = np.amin(np_bbox, axis=0)
                    max_bound = np.amax(np_bbox, axis=0)
                    new_pcd, new_index, _ = pcd.voxel_down_sample_and_trace(voxel_size, min_bound, max_bound, approximate_class=self.approximate_class)
                    index_out.append(new_index.tolist())

                pcd_out.append(new_pcd)

            return pcd_out, index_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3PointCloudDownSampleNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3PointCloudDownSampleNode)
