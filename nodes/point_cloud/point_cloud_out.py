
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.logging import info, exception
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

from sverchok_open3d.dependencies import open3d as o3d
from sverchok.utils.dummy_nodes import add_dummy

if o3d is None:
    add_dummy('SvO3PointCloudOutNode', 'Point Cloud Out', 'open3d')
else:
    class SvO3PointCloudOutNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Point Cloud Out
        Tooltip: Point Cloud Out
        """
        bl_idname = 'SvO3PointCloudOutNode'
        bl_label = 'Point Cloud Out'
        bl_icon = 'OUTLINER_OB_POINTCLOUD'
        sv_icon = 'SV_O3_POINT_CLOUD_OUT'
        methods = [
            ('STANDARD', "Standard", "Standard", 0),
            ('TANGENT', "Tangent Plane", "Tangent Plane", 1),
        ]
        normal_method: EnumProperty(
            name="Method",
            items=methods,
            default='STANDARD',
            update=updateNode)
        output_numpy: BoolProperty(
            name="Output Numpy",
            default=False,
            update=updateNode)

        def sv_init(self, context):
            self.inputs.new('SvO3PointCloudSocket', 'O3D Point Cloud').is_mandatory = True

            self.outputs.new('SvVerticesSocket', "Vertices")
            self.outputs.new('SvVerticesSocket', "Normals")
            self.outputs.new('SvColorSocket', "Colors")
        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'output_numpy')

        def process_data(self, params):

            verts_out, normals_out, color_out = [], [], []
            for pcd in params[0]:
                if self.outputs['Vertices'].is_linked:
                    verts_out.append(np.asarray(pcd.points) if self.output_numpy else np.asarray(pcd.points).tolist())
                if pcd.has_normals and self.outputs['Normals'].is_linked:
                    normals_out.append(np.asarray(pcd.normals) if self.output_numpy else np.asarray(pcd.normals).tolist())
                else:
                    normals_out.append([])
                if pcd.has_colors and self.outputs['Colors'].is_linked:
                    colors = np.asarray(pcd.colors)
                    colors_a = np.ones((colors.shape[0],4))
                    colors_a[:,:3]=colors
                    color_out.append(colors_a if self.output_numpy else colors_a.tolist())
                else:
                    color_out.append([])



            return verts_out, normals_out, color_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3PointCloudOutNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3PointCloudOutNode)
