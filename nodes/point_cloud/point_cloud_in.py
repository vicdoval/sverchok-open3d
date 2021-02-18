
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.logging import info, exception

import numpy as np
from sverchok_open3d.dependencies import open3d as o3d
from sverchok.utils.dummy_nodes import add_dummy

if o3d is None:
    add_dummy('SvO3PointCloudInNode', 'Point Cloud In', 'open3d')
else:
    class SvO3PointCloudInNode(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Point Cloud In
        Tooltip: Point Cloud In
        """
        bl_idname = 'SvO3PointCloudInNode'
        bl_label = 'Point Cloud In'
        bl_icon = 'OUTLINER_OB_EMPTY'
        sv_icon = 'SV_RANDOM_NUM_GEN'
        methods = [
            ('STANDARD', "Standard", "Standard", 0),
            ('TANGENT', "Tangent Plane", "Tangent Plane", 1),
        ]
        normal_method: EnumProperty(
            name="Method",
            items=methods,
            default='STANDARD',
            update=updateNode)
        normal_quality: IntProperty(
            name="Normal Quality",
            default=30,
            update=updateNode)
        def sv_init(self, context):
            self.inputs.new('SvVerticesSocket', "Vertices")
            self.inputs.new('SvVerticesSocket', "Normals")
            self.inputs.new('SvColorSocket', "Colors")

            self.outputs.new('SvStringsSocket', "Point Cloud")

        def draw_buttons(self, context, layout):
            if not self.inputs['Normals'].is_linked:
                layout.prop(self, 'normal_method')
                layout.prop(self, 'normal_quality')

        def process(self):

            if not self.inputs['Vertices'].is_linked:
                return

            if not self.outputs['Point Cloud'].is_linked:
                return

            vertices_s = self.inputs['Vertices'].sv_get()
            normals_s = self.inputs['Normals'].sv_get(default=[[]])
            color_s = self.inputs['Colors'].sv_get(default=[[]])



            point_clouds_out = []
            for vertices, normals, colors in zip_long_repeat(vertices_s, normals_s, color_s):
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(np.array(vertices))
                if len(normals)>0:
                    pcd.normals = o3d.utility.Vector3dVector(np.array(normals))
                else:
                    s_p = o3d.geometry.KDTreeSearchParamKNN(self.normal_quality)
                    pcd.estimate_normals(search_param=s_p)
                    if self.normal_method == 'TANGENT':
                        pcd.orient_normals_consistent_tangent_plane(self.normal_quality)


                if len(colors)>0:
                    pcd.colors = o3d.utility.Vector3dVector(np.array(colors)[:,:3])
                point_clouds_out.append(pcd)


            self.outputs['Point Cloud'].sv_set(point_clouds_out)



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3PointCloudInNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3PointCloudInNode)
