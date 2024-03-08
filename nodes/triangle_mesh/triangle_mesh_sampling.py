
import copy
import bpy
from bpy.props import EnumProperty, IntProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

from sverchok_open3d.dependencies import open3d as o3d

if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3TriangleMeshSamplingNode', 'Triangle Mesh Sampling', 'open3d')
else:
    class SvO3TriangleMeshSamplingNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: O3D Mesh Sampling
        Tooltip: Points over Open3d mesh. Mesh to Point Cloud
        """
        bl_idname = 'SvO3TriangleMeshSamplingNode'
        bl_label = 'Triangle Mesh Sampling'
        bl_icon = 'MESH_DATA'
        sv_icon = 'SV_RANDOM_NUM_GEN'
        methods = [
            ('UNIFORM', "Uniform", "Uniform Sampling", 0),
            ('POISSON', "Poisson Disk", "Poisson Disk Sampling", 1),
        ]
        normal_methods = [
            ('TRIANGLES', "From Faces", "Calculate Normals From Faces", 0),
            ('VERTEX', "From Vertex", "Calculate Normals From Vertices", 1),
            ('NONE', "None", "If mesh does not have normals, the point cloud will not have normals", 2),
        ]

        method: EnumProperty(
            name="Method",
            items=methods,
            default='POISSON',
            update=updateNode)
        normal_method: EnumProperty(
            name="Normal",
            items=normal_methods,
            default='TRIANGLES',
            update=updateNode)

        num_points: IntProperty(
            name="Point Number",
            default=100,
            update=updateNode)
        init_factor: IntProperty(
            name="Init Factor",
            description='Initial Points will be Init Factor X Number of points ',
            default=5,
            update=updateNode)
        seed: IntProperty(
            name="Seed",
            description='Random Seed Value, -1 to use a different every update',
            default=1,
            update=updateNode)

        def sv_init(self, context):
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True
            num_points = self.inputs.new('SvStringsSocket', "Points Number")
            num_points.prop_name = 'num_points'
            num_points.nesting_level = 1
            num_points.pre_processing = 'ONE_ITEM'
            seed = self.inputs.new('SvStringsSocket', "Seed")
            seed.prop_name = 'seed'
            seed.nesting_level = 1
            seed.pre_processing = 'ONE_ITEM'

            self.outputs.new('SvO3PointCloudSocket', 'O3D Point Cloud')

        def draw_buttons(self, context, layout):
            layout.prop(self, 'method')
            layout.prop(self, 'normal_method')

        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')
            self.draw_buttons(context, layout)
            if self.method == 'POISSON':
                layout.prop(self, 'init_factor')

        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")

        def process_data(self, params):

            pcd_out = []

            for mesh, points_num, seed in zip(*params):

                if self.normal_method == 'TRIANGLES':
                    use_triangle_normal = True
                elif self.normal_method == 'VERTEX':
                    use_triangle_normal = False
                    mesh = copy.deepcopy(mesh)
                    mesh.compute_vertex_normals()
                else:
                    use_triangle_normal = False
                if self.method == 'POISSON':
                    pcd = mesh.sample_points_poisson_disk(
                        points_num,
                        init_factor=self.init_factor,
                        use_triangle_normal=use_triangle_normal,
                        seed=seed)
                else:
                    pcd = mesh.sample_points_uniformly(
                        number_of_points=points_num,
                        use_triangle_normal=use_triangle_normal,
                        seed=seed)
                pcd_out.append(pcd)

            return pcd_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshSamplingNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshSamplingNode)
