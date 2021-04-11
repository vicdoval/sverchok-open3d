
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty, BoolVectorProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList, match_long_repeat
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode
from sverchok.utils.dummy_nodes import add_dummy

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import triangle_mesh_viewer_map

if o3d is None:
    add_dummy('SvO3TriangleMeshFromPointCloudNode', 'Triangle Mesh from Point Cloud', 'open3d')
else:
    class SvO3TriangleMeshFromPointCloudNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Mesh from Point Cloud
        Tooltip: Mesh from Point Cloud
        """
        bl_idname = 'SvO3TriangleMeshFromPointCloudNode'
        bl_label = 'Triangle Mesh from Point Cloud'
        bl_icon = 'MESH_DATA'
        sv_icon = 'SV_RANDOM_NUM_GEN'
        viewer_map = triangle_mesh_viewer_map
        methods = [
            ('ALPHA', "Alpha Shape", "Alpha Shape", 0),
            ('BALL_PIVOTING', "Ball Pivoting", "Ball Pivoting algorithm (Slow)", 1),
            ('POISSON', "Poisson", "Poisson Reconstruction (Fast)", 2),
        ]
        def update_sockets(self, context):
            # if self.method == 'ALPHA':
            self.inputs['Alpha'].hide_safe = self.method != 'ALPHA'
            self.inputs['Radius'].hide_safe = self.method != 'BALL_PIVOTING'
            self.inputs['Depth'].hide_safe = self.method != 'POISSON'
            self.inputs['Scale'].hide_safe = self.method != 'POISSON'
            self.inputs['Density filter'].hide_safe = self.method != 'POISSON'
            updateNode(self, context)

        method: EnumProperty(
            name="Method",
            items=methods,
            default='POISSON',
            update=update_sockets)
        alpha: FloatProperty(
            name="Alpha",
            default=2.0,
            update=updateNode)
        radius: FloatProperty(
            name="Radius",
            default=2.0,
            update=updateNode)
        depth: IntProperty(
            name="Depth",
            default=8,
            update=updateNode)
        scale: FloatProperty(
            name="Scale",
            default=1.1,
            update=updateNode)
        density_filter: FloatProperty(
            name="Min Density",
            default=0,
            update=updateNode)
        clean_faces: BoolProperty(
            name="Clean Doubled Faces",
            default=False,
            update=updateNode)
        n_threads: IntProperty(
            name="Processing Threads",
            description='Number of Processing Threads, -1 to detect automatically',
            default=-1,
            update=updateNode)
        out_np: BoolVectorProperty(
            name="Ouput Numpy",
            description="Output NumPy arrays",
            default=(False, False, False),
            size=3, update=updateNode)

        def sv_init(self, context):
            self.inputs.new('SvO3PointCloudSocket', 'O3D Point Cloud').is_mandatory = True
            alpha = self.inputs.new('SvStringsSocket', "Alpha")
            alpha.prop_name = 'alpha'
            alpha.nesting_level = 1
            alpha.pre_processing = 'ONE_ITEM'
            radius = self.inputs.new('SvStringsSocket', "Radius")
            radius.prop_name = 'radius'
            radius.nesting_level = 1
            radius.pre_processing = 'ONE_ITEM'
            depth = self.inputs.new('SvStringsSocket', "Depth")
            depth.prop_name = 'depth'
            depth.nesting_level = 1
            depth.pre_processing = 'ONE_ITEM'
            scale = self.inputs.new('SvStringsSocket', "Scale")
            scale.prop_name = 'scale'
            scale.nesting_level = 1
            scale.pre_processing = 'ONE_ITEM'
            density_filter = self.inputs.new('SvStringsSocket', "Density filter")
            density_filter.prop_name = 'density_filter'
            density_filter.pre_processing = 'ONE_ITEM'
            density_filter.nesting_level = 1
            self.inputs['Alpha'].hide_safe = True
            self.inputs['Radius'].hide_safe = True

            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")
            self.outputs.new('SvStringsSocket', "Density")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'method')

        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')
            self.draw_buttons(context, layout)
            layout.prop(self, 'n_threads')

        def rclick_menu(self, context, layout):
            '''right click sv_menu items'''
            layout.prop_menu_enum(self, "method")
            layout.prop_menu_enum(self, "list_match")

        def process_data(self, params):

            omesh, ovals = [], []
            for pcd, alpha, radius, depth, scale, density_filter in zip(*params):
                vals = []
                if self.method == 'ALPHA':
                    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
                elif self.method == 'BALL_PIVOTING':
                    radi = o3d.utility.DoubleVector(np.array([radius]))
                    if not pcd.has_normals():
                        pcd.estimate_normals()
                    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, radi)
                else:
                    if not pcd.has_normals():
                        pcd.estimate_normals()
                    mesh, vals = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=depth, scale=scale, n_threads=self.n_threads)
                    if density_filter > 0:
                        vals = np.asarray(vals)
                        mask = vals < density_filter
                        mesh.remove_vertices_by_mask(mask)
                        vals = vals[mask]

                omesh.append(mesh)
                ovals.append(vals)

            return omesh, ovals



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshFromPointCloudNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshFromPointCloudNode)
