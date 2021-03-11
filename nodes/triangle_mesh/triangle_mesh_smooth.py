
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
    add_dummy('SvO3TriangleMeshSmoothNode', 'O3D Triangle Mesh Smooth', 'open3d')
else:
    class SvO3TriangleMeshSmoothNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: Triangle Mesh Smooth
        Tooltip: Open3d Triangle Mesh Smooth
        """
        bl_idname = 'SvO3TriangleMeshSmoothNode'
        bl_label = 'Triangle Mesh Smooth'
        bl_icon = 'MESH_DATA'
        sv_icon = 'SV_RANDOM_NUM_GEN'
        methods = [
            ('simple', "Simple", "Smooth mesh using simple algorithm", 0),
            ('laplacian', "Laplacian", "Smooth mesh using laplacian algorithm", 1),
            ('taubin', "Taubin", "Smooth mesh using Taubin algorithm", 2),
        ]

        method: EnumProperty(
            name="Method",
            items=methods,
            default='simple',
            update=updateNode)
        iterations: IntProperty(
            name="Iterations",
            default=1,
            min=0,
            update=updateNode)
        filter_lambda: FloatProperty(
             name="Lambda",
             default=0.5,
             update=updateNode)
        filter_mu: FloatProperty(
             name="Mu",
             default=0.53,
             update=updateNode)




        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True
            self.inputs.new('SvStringsSocket', "Iterations").prop_name = 'iterations'
            self.inputs.new('SvStringsSocket', "Lambda").prop_name = 'filter_lambda'
            self.inputs.new('SvStringsSocket', "Mu").prop_name = 'filter_mu'
            for s in self.inputs[1:]:
                s.nesting_level = 1
                s.pre_processing = 'ONE_ITEM'
            self.inputs['Lambda'].hide_safe=True
            self.inputs['Mu'].hide_safe=True

            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'method')


        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')
            self.draw_buttons(context, layout)

        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")


        def process_data(self, params):

            mesh_out = []

            for mesh, iterations, filter_lambda, filter_mu in zip(*params):
                if iterations < 1:
                    mesh_new = mesh
                else:
                    if self.method == 'simple':
                        mesh_new = mesh.filter_smooth_simple(number_of_iterations=iterations)
                    elif self.method == 'laplacian':
                        mesh_new = mesh.filter_smooth_laplacian(number_of_iterations=iterations)#, lambda=filter_lamda)
                    else:
                        mesh_new = mesh.filter_smooth_taubin(number_of_iterations=iterations)#,lambda=filter_lamda, mu=filter_mu)

                mesh_out.append(mesh_new)


            return mesh_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshSmoothNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshSmoothNode)
