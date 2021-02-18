
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty, BoolVectorProperty
from mathutils import Matrix

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat, fullList, match_long_repeat
from sverchok.utils.logging import info, exception
from sverchok.utils.sv_mesh_utils import polygons_to_edges_np
import numpy as np
from sverchok_open3d.dependencies import open3d as o3d
from sverchok.utils.dummy_nodes import add_dummy

def clean_doubled_faces(faces):
    faces_o = np.sort(faces)
    faces_o, idx = np.unique(faces_o, axis=0, return_index=True)
    return faces[idx]

if o3d is None:
    add_dummy('SvO3MeshFrom3PointCloudNode', 'Mesh from Point Cloud', 'open3d')
else:
    socket_names = ['Vertices', 'Edges', 'Polygons']
    class SvO3MeshFrom3PointCloudNode(bpy.types.Node, SverchCustomTreeNode):
        """
        Triggers: Mesh from Point Cloud
        Tooltip: Mesh from Point Cloud
        """
        bl_idname = 'SvO3MeshFrom3PointCloudNode'
        bl_label = 'Mesh from Point Cloud'
        bl_icon = 'OUTLINER_OB_EMPTY'
        sv_icon = 'SV_RANDOM_NUM_GEN'

        methods = [
            ('ALPHA', "Alpha Shape", "Simplest Euler method", 0),
            ('BALL_PIVOTING', "Ball Pivoting", "Runge-Kutta 5(4)", 1),
            ('POISSON', "Poisson", "Runge-Kutta 3(2)", 2),
        ]
        def update_sockets(self, context):
            # if self.method == 'ALPHA':
            self.inputs['Alpha'].hide_safe = self.method != 'ALPHA'
            self.inputs['Radius'].hide_safe = self.method != 'BALL_PIVOTING'
            self.inputs['Depth'].hide_safe = self.method != 'POISSON'
            self.inputs['Scale'].hide_safe = self.method != 'POISSON'
            updateNode(self, context)

        method: EnumProperty(
            name="Method",
            items=methods,
            default='ALPHA',
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
        clean_faces: BoolProperty(
            name="Clean Doubled Faces",
            default=False,
            update=updateNode)
        out_np: BoolVectorProperty(
            name="Ouput Numpy",
            description="Output NumPy arrays",
            default=(False, False, False),
            size=3, update=updateNode)

        def sv_init(self, context):
            self.inputs.new('SvStringsSocket', "Point Cloud")
            self.inputs.new('SvStringsSocket', "Alpha").prop_name = 'alpha'
            self.inputs.new('SvStringsSocket', "Radius").prop_name = 'radius'
            self.inputs.new('SvStringsSocket', "Depth").prop_name = 'depth'
            self.inputs.new('SvStringsSocket', "Scale").prop_name = 'scale'


            self.outputs.new('SvVerticesSocket', "Vertices")
            self.outputs.new('SvStringsSocket', "Edges")
            self.outputs.new('SvStringsSocket', "Faces")
            self.outputs.new('SvStringsSocket', "Density")
            self.outputs.new('SvStringsSocket', "O3d Mesh")

        def draw_buttons(self, context, layout):
            layout.prop(self, 'method')
            layout.prop(self, 'clean_faces')

        def draw_buttons_ext(self, context, layout):
            self.draw_buttons(context, layout)
            layout.label(text="Ouput Numpy:")
            r = layout.row()
            for i in range(3):
                r.prop(self, "out_np", index=i, text=socket_names[i], toggle=True)
        def rclick_menu(self, context, layout):
            '''right click sv_menu items'''
            layout.prop_menu_enum(self, "method")
            layout.prop(self, 'clean_faces')
            layout.label(text="Ouput Numpy:")
            for i in range(3):
                layout.prop(self, "out_np", index=i, text=socket_names[i], toggle=True)
        def process(self):

            if not self.inputs['Point Cloud'].is_linked:
                return

            if not any([s.is_linked for s in self.outputs]):
                return


            params = [self.inputs['Point Cloud'].sv_get()]
            for s in self.inputs[1:]:
                params.append(s.sv_get(default=[[]])[0])
            matched = match_long_repeat
            get_verts, get_edges, get_faces = [s.is_linked for s in self.outputs[:3]]
            overts, oedges, ofaces, omesh, ovals = [], [], [], [], []
            for pcd, alpha, radius, depth, scale in zip(*matched(params)):
                vals = []
                if self.method == 'ALPHA':
                    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd,alpha)
                elif self.method == 'BALL_PIVOTING':
                    radi = o3d.utility.DoubleVector(np.array([radius]))
                    if not pcd.has_normals():
                        pcd.estimate_normals()
                    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,radi)
                else:
                    if not pcd.has_normals():
                        pcd.estimate_normals()
                    mesh, vals = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=depth, scale=scale)

                if get_verts:
                    overts.append(np.asarray(mesh.vertices) if self.out_np[0] else np.asarray(mesh.vertices).tolist())

                if get_faces or get_edges:
                    if self.clean_faces:
                        faces = clean_doubled_faces(np.asarray(mesh.triangles))
                        if get_faces:
                            ofaces.append(faces if self.out_np[2] else faces.tolist())
                        if get_edges:
                            edges = polygons_to_edges_np([faces], unique_edges=True, output_numpy=self.out_np[1])[0]
                            oedges.append(edges)
                    else:
                        if not get_edges:
                            ofaces.append(np.asarray(mesh.triangles) if self.out_np[2] else np.asarray(mesh.triangles).tolist())
                        else:
                            faces = np.asarray(mesh.triangles)
                            edges = polygons_to_edges_np([faces], unique_edges=True, output_numpy=self.out_np[1])[0]
                            oedges.append(edges)
                            if get_faces:
                                ofaces.append(faces if self.out_np[2] else faces.tolist())


                if self.outputs['O3d Mesh'].is_linked:
                    omesh.append(mesh)
                if self.outputs['Density'].is_linked:
                    ovals.append(np.asarray(vals))

            self.outputs['Vertices'].sv_set(overts)
            self.outputs['Edges'].sv_set(oedges)
            self.outputs['Faces'].sv_set(ofaces)
            self.outputs['Density'].sv_set(ovals)
            self.outputs['O3d Mesh'].sv_set(omesh)



def register():
    if o3d is not None:
        bpy.utils.register_class(SvO3MeshFrom3PointCloudNode)

def unregister():
    if o3d is not None:
        bpy.utils.unregister_class(SvO3MeshFrom3PointCloudNode)
