
import copy
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList
from sverchok.utils.nodes_mixins.recursive_nodes import SvRecursiveNode

from sverchok_open3d.dependencies import open3d as o3d
from sverchok_open3d.utils.triangle_mesh import triangle_mesh_viewer_map

if o3d is None:
    from sverchok.utils.dummy_nodes import add_dummy
    add_dummy('SvO3TriangleMeshDeformAsRigidNode', 'Triangle Mesh Deform as Rigid', 'open3d')
else:
    class SvO3TriangleMeshDeformAsRigidNode(bpy.types.Node, SverchCustomTreeNode, SvRecursiveNode):
        """
        Triggers: ARAP As Rigid as Possible
        Tooltip: Deforms triangle Mesh as rigid as possible
        """
        bl_idname = 'SvO3TriangleMeshDeformAsRigidNode'
        bl_label = 'Triangle Mesh Deform as Rigid'
        bl_icon = 'MESH_DATA'

        viewer_map = triangle_mesh_viewer_map
        methods = [
            ('SPOKES', "Spokes", "Spokes", 0),
            ('SMOOTHED', "Smoothed", "Smoothed", 1),

        ]

        energy_mode: EnumProperty(
            name="Energy Mode",
            description='Energy model that is minimized in the deformation process',
            items=methods,
            default='SPOKES',
            update=updateNode)


        max_iterations: IntProperty(
            name="Max Iterations",
            description='Maximum number of iterations to minimize energy functional',
            default=5,
            min=0,
            update=updateNode)
        smoothed_alpha: FloatProperty(
            name="Smoothed Alpha",
            description='trade-off parameter for the smoothed energy functional for the regularization term',
            default=0.01,
            update=updateNode)



        def sv_init(self, context):
            self.width = 200
            self.inputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh").is_mandatory = True
            self.inputs.new('SvStringsSocket', "Pins Index").is_mandatory = True
            self.inputs.new('SvVerticesSocket', "Pins Position").is_mandatory = True
            self.inputs.new('SvStringsSocket', "Max Iterations").prop_name = 'max_iterations'
            self.inputs.new('SvStringsSocket', "Smoothed Alpha").prop_name = 'smoothed_alpha'
            for s in self.inputs[3:]:
                s.nesting_level = 1
                s.pre_processing = 'ONE_ITEM'

            self.outputs.new('SvO3TriangleMeshSocket', "O3D Triangle Mesh")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'energy_mode')


        def draw_buttons_ext(self, context, layout):
            layout.prop(self, 'list_match')
            self.draw_buttons(context, layout)

        def rclick_menu(self, context, layout):
            layout.prop_menu_enum(self, "list_match", text="List Match")


        def process_data(self, params):

            mesh_out = []
            vec_3f = o3d.utility.Vector3dVector
            int_list = o3d.utility.IntVector
            if self.energy_mode == 'SPOKES':
                energy_mode = o3d.geometry.DeformAsRigidAsPossibleEnergy.Spokes
            else:
                energy_mode = o3d.geometry.DeformAsRigidAsPossibleEnergy.Smoothed
            for mesh, vert_index, vert_pos, max_iterations, smoothed_alpha in zip(*params):
                mesh_new = copy.deepcopy(mesh)
                mesh_new = mesh.deform_as_rigid_as_possible(
                    int_list(np.array(vert_index)),
                    vec_3f(np.array(vert_pos)),
                    max_iterations,
                    energy=energy_mode,
                    smoothed_alpha=smoothed_alpha)

                mesh_out.append(mesh_new)


            return mesh_out



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3TriangleMeshDeformAsRigidNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3TriangleMeshDeformAsRigidNode)
