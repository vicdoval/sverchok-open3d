
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty, StringProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.logging import info, exception

import numpy as np
from sverchok_open3d.dependencies import open3d as o3d
from sverchok.utils.dummy_nodes import add_dummy

if o3d is None:
    add_dummy('SvO3PointCloudImportNode', 'Point Cloud Import', 'open3d')
else:
    class SvExportPointCloudOperator(bpy.types.Operator):

        bl_idname = "node.sv_export_point_cloud"
        bl_label = "Export Point Cloud"
        bl_options = {'INTERNAL', 'REGISTER'}

        idtree: StringProperty(default='')
        idname: StringProperty(default='')

        def execute(self, context):
            tree = bpy.data.node_groups[self.idtree]
            node = bpy.data.node_groups[self.idtree].nodes[self.idname]

            if not node.inputs['Folder Path'].is_linked:
                self.report({'WARNING'}, "Folder path is not specified")
                return {'FINISHED'}
            if not node.inputs['Point Cloud'].is_linked:
                self.report({'WARNING'}, "Point Cloud to be exported is not specified")
                return {'FINISHED'}

            folder_path = node.inputs[0].sv_get()[0][0]
            point_cloud_in = node.inputs['Point Cloud'].sv_get()

            base_name = node.base_name
            if not base_name:
                base_name = "sv_point_cloud"

            for i, pcd in enumerate(point_cloud_in):
                file_path = folder_path + base_name + "_"  + "%05d" % i + ".ply"
                o3d.io.write_point_cloud(file_path, pcd, write_ascii=node.write_ascii, compressed=node.compressed, print_progress=node.print_progress)

                self.report({'INFO'}, f"Saved object #{i} to {file_path}")

            return {'FINISHED'}

    class SvO3PointCloudExportNode(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Point Cloud Export
        Tooltip: Point Cloud Export
        """
        bl_idname = 'SvO3PointCloudExportNode'
        bl_label = 'Point Cloud Export'
        bl_icon = 'OUTLINER_OB_EMPTY'
        sv_icon = 'SV_RANDOM_NUM_GEN'

        write_ascii: BoolProperty(
            name="Write Ascii",
            default=True,
            update=updateNode)
        compressed: BoolProperty(
            name="Compressed",
            default=True,
            update=updateNode)
        print_progress: BoolProperty(
            name="Print Progress in console",
            default=False,
            update=updateNode)
        base_name: StringProperty(
            name="Base Name",
            description="Name of file",
            )

        def sv_init(self, context):
            self.inputs.new('SvFilePathSocket', "Folder Path")
            self.inputs.new('SvStringsSocket', "Point Cloud")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'write_ascii')
            layout.prop(self, 'compressed')
            layout.prop(self, 'print_progress')
            layout.prop(self, "base_name")
            self.wrapper_tracked_ui_draw_op(layout, SvExportPointCloudOperator.bl_idname, icon='EXPORT', text="EXPORT")

        def process(self):
            pass




def register():
    if o3d is not None:
        bpy.utils.register_class(SvExportPointCloudOperator)
        bpy.utils.register_class(SvO3PointCloudExportNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3PointCloudExportNode)
        bpy.utils.unregister_class(SvExportPointCloudOperator)
