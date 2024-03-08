
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.sv_logging import sv_logger

import numpy as np
from sverchok_open3d.dependencies import open3d as o3d

if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3ImportNode', 'Open3D Import', 'open3d')
else:

    class SvO3ImportNode(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Point Cloud or TriangleMesh
        Tooltip: Import from file Point Cloud or TriangleMesh
        """
        bl_idname = 'SvO3ImportNode'
        bl_label = 'Open3D Import'
        bl_icon = 'IMPORT'

        import_types = [
            ('triangle_mesh', "Triangle Mesh", "Triangle Mesh", 0),
            ('point_cloud', "Point Cloud", "Point Cloud", 1),
        ]
        def update_sockets(self, context):
            self.outputs["O3D Point Cloud"].hide_safe = self.import_type == 'triangle_mesh'
            self.outputs["O3D Triangle Mesh"].hide_safe = self.import_type == 'point_cloud'
        import_type: EnumProperty(
            name="Import",
            items=import_types,
            default='point_cloud',
            update=update_sockets)

        remove_nan_points: BoolProperty(
            name="Remove NaN points",
            default=True,
            update=updateNode)
        remove_infinite_points: BoolProperty(
            name="Remove Infinite points",
            default=True,
            update=updateNode)
        enable_post_processing: BoolProperty(
            name="Enable Postprocessing",
            default=False,
            update=updateNode)
        print_progress: BoolProperty(
            name="Print Progress in console",
            default=False,
            update=updateNode)
        def sv_init(self, context):
            self.inputs.new('SvFilePathSocket', "File Path")
            self.outputs.new('SvO3PointCloudSocket', 'O3D Point Cloud')
            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").hide_safe = True


        def draw_buttons(self, context, layout):

            layout.prop(self, 'import_type')
            if self.import_type == 'point_cloud':
                layout.prop(self, 'remove_nan_points')
                layout.prop(self, 'remove_infinite_points')
            else:
                layout.prop(self, 'enable_post_processing')
            layout.prop(self, 'print_progress')

        def process(self):

            if not self.inputs['File Path'].is_linked:
                return

            if not any([s.is_linked for s in self.outputs]):
                return

            files_s = self.inputs['File Path'].sv_get()

            point_clouds_out, mesh_out = [], []
            for files in files_s:
                for file in files:
                    if self.import_type == 'point_cloud':
                        pcd = o3d.io.read_point_cloud(
                            file,
                            remove_nan_points=self.remove_nan_points,
                            remove_infinite_points=self.remove_infinite_points,
                            print_progress=self.print_progress)
                        point_clouds_out.append(pcd)
                    else:
                        mesh = o3d.io.read_triangle_mesh(
                            file,
                            enable_post_processing =self.enable_post_processing ,
                            print_progress=self.print_progress)
                        mesh_out.append(mesh)

            self.outputs['O3D Point Cloud'].sv_set(point_clouds_out)
            self.outputs['O3D Triangle Mesh'].sv_set(mesh_out)



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3ImportNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3ImportNode)
