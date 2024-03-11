
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty, StringProperty
from mathutils import Matrix
from bpy.props import StringProperty

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.sv_logging import sv_logger

import numpy as np
from sverchok_open3d.dependencies import open3d as o3d

class SvO3ExportOperator(bpy.types.Operator):

    bl_idname = "node.sv_export_open3d"
    bl_label = "Open3d Export"
    bl_options = {'INTERNAL', 'REGISTER'}
    sv_dependencies = ['open3d']

    node_name : StringProperty()
    tree_name: StringProperty()

    idtree: StringProperty(default='')
    idname: StringProperty(default='')

    def execute(self, context):
        tree = bpy.data.node_groups[self.idtree]
        node = bpy.data.node_groups[self.idtree].nodes[self.idname]

        if not node.inputs['Folder Path'].is_linked:
            self.report({'WARNING'}, "Folder path is not specified")
            return {'FINISHED'}


        folder_path = node.inputs[0].sv_get()[0][0]
        base_name = node.base_name
        if node.export_type == 'point_cloud':
            if not node.inputs['O3D Point Cloud'].is_linked:
                self.report({'WARNING'}, "Point Cloud to be exported is not specified")
                return {'FINISHED'}
            point_cloud_in = node.inputs['O3D Point Cloud'].sv_get()

            if not base_name:
                base_name = "sv_point_cloud"
            pcd_flat = node.inputs['O3D Point Cloud'].do_flatten(point_cloud_in)

            for i, pcd in enumerate(pcd_flat):
                file_path = folder_path + base_name + "_"  + "%05d" % i + ".ply"
                o3d.io.write_point_cloud(file_path, pcd, write_ascii=node.write_ascii, compressed=node.compressed, print_progress=node.print_progress)

                self.report({'INFO'}, f"Saved object #{i} to {file_path}")
        else:
            if not node.inputs['Triangle Mesh'].is_linked:
                self.report({'WARNING'}, "Triangle Mesh to be exported is not specified")
                return {'FINISHED'}
            mesh_in = node.inputs['O3D Triangle Mesh'].sv_get()
            if not base_name:
                base_name = "sv_triangle_mesh"
            mesh_flat = node.inputs['O3D Triangle Mesh'].do_flatten(mesh_in)
            for i, mesh in enumerate(mesh_flat):
                file_path = folder_path + base_name + "_"  + "%05d" % i + ".obj"
                o3d.io.write_triangle_mesh(
                    file_path,
                    mesh,
                    write_ascii=node.write_ascii,
                    compressed=node.compressed,
                    write_vertex_normals=node.write_vertex_normals,
                    write_vertex_colors=node.write_vertex_colors,
                    write_triangle_uvs=node.write_triangle_uvs,
                    print_progress=node.print_progress)

                self.report({'INFO'}, f"Saved object #{i} to {file_path}")

        return {'FINISHED'}

class SvO3ExportNode(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Point Cloud or TriangleMesh
    Tooltip: Export file Point Cloud or TriangleMesh
    """
    bl_idname = 'SvO3ExportNode'
    bl_label = 'Open3D Export'
    bl_icon = 'EXPORT'
    sv_dependencies = ['open3d']

    export_types = [
        ('triangle_mesh', "Triangle Mesh", "Triangle Mesh", 0),
        ('point_cloud', "Point Cloud", "Point Cloud", 1),
    ]
    def update_sockets(self, context):
        self.inputs["Point Cloud"].hide_safe = self.export_type == 'triangle_mesh'
        self.inputs["O3D Triangle Mesh"].hide_safe = self.export_type == 'point_cloud'
    export_type: EnumProperty(
        name="Export",
        items=export_types,
        default='triangle_mesh',
        update=update_sockets)

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

    write_vertex_normals: BoolProperty(
        name='Write Vertex Normals',
        default=True,
        description= 'Set to False to not write any vertex normals, even if present on the mesh',
        update=updateNode)
    write_vertex_colors: BoolProperty(
        name='Write Vertex Colors',
        default=True,
        description= 'Set to False to not write any vertex colors, even if present on the mesh',
        update=updateNode)
    write_triangle_uvs: BoolProperty(
        name='Write Triangle UVs',
        default=True,
        description= 'Set to False to not write any triangle uvs, even if present on the mesh. For obj format, mtl file is saved only when True is set',
        update=updateNode)

    base_name: StringProperty(
        name="Base Name",
        description="Name of file",
        )

    def sv_init(self, context):
        self.inputs.new('SvFilePathSocket', "Folder Path")
        self.inputs.new('SvO3PointCloudSocket', 'O3D Point Cloud')
        self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'export_type')
        layout.prop(self, 'write_ascii')
        layout.prop(self, 'compressed')
        if self.export_type == 'triangle_mesh':
            layout.prop(self, 'write_vertex_normals')
            layout.prop(self, 'write_vertex_colors')
            layout.prop(self, 'write_triangle_uvs')

        layout.prop(self, 'print_progress')
        layout.prop(self, "base_name")
        self.wrapper_tracked_ui_draw_op(layout, SvO3ExportOperator.bl_idname, icon='EXPORT', text="EXPORT")

    def process(self):
        pass

def register():
    bpy.utils.register_class(SvO3ExportOperator)
    bpy.utils.register_class(SvO3ExportNode)

def unregister():
    bpy.utils.unregister_class(SvO3ExportNode)
    bpy.utils.unregister_class(SvO3ExportOperator)
