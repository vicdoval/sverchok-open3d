
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

class SvO3PointCloudImportNode(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Point Cloud Import
    Tooltip: Point Cloud Import
    """
    bl_idname = 'SvO3PointCloudImportNode'
    bl_label = 'Point Cloud Import'
    bl_icon = 'OUTLINER_OB_EMPTY'
    sv_icon = 'SV_RANDOM_NUM_GEN'
    sv_dependencies = ['open3d']

    remove_nan_points: BoolProperty(
        name="Remove NaN points",
        default=True,
        update=updateNode)
    remove_infinite_points: BoolProperty(
        name="Remove Infinite points",
        default=True,
        update=updateNode)
    print_progress: BoolProperty(
        name="Print Progress in console",
        default=False,
        update=updateNode)
    def sv_init(self, context):
        self.inputs.new('SvFilePathSocket', "File Path")
        self.outputs.new('SvStringsSocket', "Point Cloud")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'remove_nan_points')
        layout.prop(self, 'remove_infinite_points')
        layout.prop(self, 'print_progress')

    def process(self):

        if not self.inputs['File Path'].is_linked:
            return

        if not self.outputs['Point Cloud'].is_linked:
            return

        files_s = self.inputs['File Path'].sv_get()

        point_clouds_out = []
        for files in files_s:
            for file in files:
                pcd = o3d.io.read_point_cloud(
                    file,
                    remove_nan_points=self.remove_nan_points,
                    remove_infinite_points=self.remove_infinite_points,
                    print_progress=self.print_progress)
                point_clouds_out.append(pcd)


        self.outputs['Point Cloud'].sv_set(point_clouds_out)



def register():
    bpy.utils.register_class(SvO3PointCloudImportNode)

def unregister():
    bpy.utils.unregister_class(SvO3PointCloudImportNode)
