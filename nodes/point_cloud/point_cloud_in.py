
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
from sverchok_open3d.utils.point_cloud import calc_point_cloud_normals
if o3d is None:
    add_dummy('SvO3PointCloudInNode', 'Point Cloud In', 'open3d')
else:
    class SvO3PointCloudInNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Point Cloud In
        Tooltip: Point Cloud In
        """
        bl_idname = 'SvO3PointCloudInNode'
        bl_label = 'Point Cloud In'
        bl_icon = 'OUTLINER_OB_POINTCLOUD'
        sv_icon = 'SV_O3_POINT_CLOUD_IN'
        methods = [
            ('STANDARD', "Standard", "Standard", 0),
            ('TANGENT', "Tangent Plane", "Better results with more processing time", 1),
            ('NONE', "None", "Do not calculate them", 2),
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
        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvVerticesSocket', "Vertices").is_mandatory = True

            self.inputs.new('SvVerticesSocket', "Normals").nesting_level = 3
            self.inputs.new('SvColorSocket', "Colors").nesting_level = 3

            self.outputs.new('SvO3PointCloudSocket', 'O3D Point Cloud')

        def draw_buttons(self, context, layout):
            if not self.inputs['Normals'].is_linked:
                layout.prop(self, 'normal_method')
                layout.prop(self, 'normal_quality')

        def process_data(self, params):

            point_clouds_out = []
            for vertices, normals, colors in zip(*params):
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(np.array(vertices))
                if len(normals)>0:
                    pcd.normals = o3d.utility.Vector3dVector(np.array(normals))
                elif self.normal_method != 'NONE':
                    calc_point_cloud_normals(pcd, self.normal_quality, self.normal_method)



                if len(colors) > 0:
                    pcd.colors = o3d.utility.Vector3dVector(np.array(colors)[:,:3])
                point_clouds_out.append(pcd)


            return point_clouds_out


def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3PointCloudInNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3PointCloudInNode)
