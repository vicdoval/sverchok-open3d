
import numpy as np
import copy
import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.sv_logging import sv_logger
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode


from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.point_cloud import calc_point_cloud_normals
if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3PointCloudCalcNormalsNode', 'Point Cloud Calc Normals', 'open3d')
else:
    class SvO3PointCloudCalcNormalsNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Point Cloud Calc Normals
        Tooltip:  Calculate Normals of Point Cloud
        """
        bl_idname = 'SvO3PointCloudCalcNormalsNode'
        bl_label = 'Point Cloud Calc Normals'
        bl_icon = 'OUTLINER_OB_POINTCLOUD'
        sv_icon = 'SV_RANDOM_NUM_GEN'
        methods = [
            ('STANDARD', "Standard", "Standard", 0),
            ('TANGENT', "Tangent Plane", "Better results with more processing time", 1),

        ]
        normal_method: EnumProperty(
            name="Normal Method",
            description='Method used to calculate normals if not supplied',
            items=methods,
            default='STANDARD',
            update=updateNode)
        normal_quality: IntProperty(
            name="Normal Quality",
            default=30,
            min=1,
            update=updateNode)
        output_numpy: BoolProperty(
            name="Output Numpy",
            default=False,
            update=updateNode)

        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3PointCloudSocket', "O3D Point Cloud").is_mandatory = True
            quality = self.inputs.new('SvStringsSocket', "Quality")
            quality.prop_name = 'normal_quality'
            quality.nesting_level = 1
            quality.pre_processing = 'ONE_ITEM'

            self.outputs.new('SvO3PointCloudSocket', 'O3D Point Cloud')
            self.outputs.new('SvVerticesSocket', "Normals")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'normal_method')

        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)
            layout.prop(self, 'output_numpy')


        def process_data(self, params):

            point_clouds_out, normals_out = [], []
            for pcd, quality in zip(*params):
                new_pcd = copy.deepcopy(pcd)

                calc_point_cloud_normals(new_pcd, quality, self.normal_method)
                normals_out.append(np.asarray(new_pcd.normals) if self.output_numpy else np.asarray(new_pcd.normals).tolist())
                point_clouds_out.append(new_pcd)


            return point_clouds_out, normals_out


def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3PointCloudCalcNormalsNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3PointCloudCalcNormalsNode)
