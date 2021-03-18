
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty
from mathutils import Matrix
import copy
import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.logging import info, exception
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

import numpy as np
from sverchok_open3d.dependencies import open3d as o3d
from sverchok.utils.dummy_nodes import add_dummy

if o3d is None:
    add_dummy('SvO3TriangleMeshSimplifyNode', 'Triangle Mesh Simplify', 'open3d')
else:
    class SvO3TriangleMeshSimplifyNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: O3D Mesh Sampling
        Tooltip: Points over Open3d mesh. Mesh to Point Cloud
        """
        bl_idname = 'SvO3TriangleMeshSimplifyNode'
        bl_label = 'Triangle Mesh Simplify'
        bl_icon = 'MESH_DATA'

        methods = [
            ('quadric_decimation', "Quadric Decimation", "Quadric Decimation", 0),
            ('vertex_clustering', "Vertex Clustering", "Vertex Clustering", 1),
            ('merge_by_distance', "Merge By Distance", "Merge By Distance", 2),
        ]
        contraction_methods = [
            ('Average', "Average", "The vertex positions are computed by the averaging", 0),
            ('Quadric', "Quadric", "The vertex positions are computed by minimizing the distance to the adjacent triangle planes", 1),
        ]
        def update_sockets_and_update(self, context):
            self.update_sockets()
            updateNode(self, context)
        def update_sockets(self):
            self.inputs['Triangle Number'].hide_safe = self.method != 'quadric_decimation'
            self.inputs['Boundary Weight'].hide_safe = self.method != 'quadric_decimation'
            self.inputs['Voxel Size'].hide_safe = self.method != 'vertex_clustering'
            self.inputs['Distance'].hide_safe = self.method != 'merge_by_distance'
        method: EnumProperty(
            name="Method",
            items=methods,
            default='quadric_decimation',
            update=update_sockets_and_update)
        target_number_of_triangles: IntProperty(
            name="Triangle Number",
            default=100,
            update=updateNode)
        boundary_weight: FloatProperty(
            name="Boundary Weight",
            default=1,
            update=updateNode)
        voxel_size: FloatProperty(
            name="Voxel Size",
            description='The size of the voxel within vertices are pooled',
            default=5,
            update=updateNode)
        distance: FloatProperty(
            name="Distance",
            description='Vertices under this distance will be merged',
            default=0.1,
            update=updateNode)
        contraction: EnumProperty(
            name="Contraction Method",
            items=contraction_methods,
            default='Average',
            update=updateNode)


        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True
            self.inputs.new('SvStringsSocket', "Triangle Number").prop_name = 'target_number_of_triangles'
            self.inputs.new('SvStringsSocket', "Boundary Weight").prop_name = 'boundary_weight'
            self.inputs.new('SvStringsSocket', "Voxel Size").prop_name = 'voxel_size'
            self.inputs.new('SvStringsSocket', "Distance").prop_name = 'distance'
            for s in self.inputs[1:]:
                s.nesting_level = 1
                s.pre_processing = 'ONE_ITEM'
            self.update_sockets()
            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'method')
            if self.method == 'vertex_clustering':
                layout.prop(self, 'contraction')

        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')
            self.draw_buttons(context, layout)

        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")


        def process_data(self, params):

            mesh_out = []

            for mesh, num_of_triangles, boundary_weight, voxel_size, distance in zip(*params):
                mesh_new = copy.deepcopy(mesh)
                if self.method == 'quadric_decimation':
                    mesh_new = mesh_new.simplify_quadric_decimation(num_of_triangles, boundary_weight=boundary_weight)

                elif self.method == 'vertex_clustering':
                    if self.contraction == 'Average':
                        contraction = o3d.geometry.SimplificationContraction.Average
                    else:
                        contraction = o3d.geometry.SimplificationContraction.Quadric
                    mesh_new = mesh_new.simplify_vertex_clustering(voxel_size, contraction=contraction)
                else:
                    mesh_new = mesh_new.merge_close_vertices(distance)
                    mesh_new = mesh_new.remove_degenerate_triangles()
                    mesh_new = mesh_new.remove_duplicated_triangles()
                mesh_out.append(mesh_new)


            return mesh_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshSimplifyNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshSimplifyNode)
