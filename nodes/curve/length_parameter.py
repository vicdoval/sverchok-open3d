import numpy as np

from mathutils import Matrix
import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty

from sverchok.node_tree import SverchCustomTreeNode, throttled
from sverchok.data_structure import updateNode, zip_long_repeat, ensure_nesting_level
from sverchok.utils.geom import LinearSpline, CubicSpline

class SvExCurveLengthParameterNode(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Curve Length Parameter
    Tooltip: Solve curve length (natural) parameter
    """
    bl_idname = 'SvExCurveLengthParameterNode'
    bl_label = 'Curve Length Parameter'
    bl_icon = 'MESH_CIRCLE'

    resolution : IntProperty(
        name = 'Resolution',
        min = 1,
        default = 50,
        update = updateNode)

    length : FloatProperty(
        name = "Length",
        min = 0.0,
        default = 0.5,
        update = updateNode)

    modes = [('SPL', 'Cubic', "Cubic Spline", 0),
             ('LIN', 'Linear', "Linear Interpolation", 1)]

    mode: EnumProperty(name='Mode', default="SPL", items=modes, update=updateNode)

    @throttled
    def update_sockets(self, context):
        self.inputs['Length'].hide_safe = self.eval_mode != 'MANUAL'
        self.inputs['Samples'].hide_safe = self.eval_mode != 'AUTO'

    eval_modes = [
        ('AUTO', "Automatic", "Evaluate the curve at evenly spaced points", 0),
        ('MANUAL', "Manual", "Evaluate the curve at specified points", 1)
    ]

    eval_mode : EnumProperty(
        name = "Mode",
        items = eval_modes,
        default = 'AUTO',
        update = update_sockets)

    sample_size : IntProperty(
            name = "Samples",
            default = 50,
            min = 4,
            update = updateNode)

    def sv_init(self, context):
        self.inputs.new('SvExCurveSocket', "Curve").display_shape = 'DIAMOND'
        self.inputs.new('SvStringsSocket', "Resolution").prop_name = 'resolution'
        self.inputs.new('SvStringsSocket', "Length").prop_name = 'length'
        self.inputs.new('SvStringsSocket', "Samples").prop_name = 'sample_size'
        self.outputs.new('SvStringsSocket', "T")
        self.outputs.new('SvVerticesSocket', "Vertices")
        self.update_sockets(context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'mode', expand=True)
        layout.prop(self, 'eval_mode', expand=True)

    def make_spline(self, tknots, length_params):
        zeros = np.zeros(len(tknots))
        control_points = np.vstack((length_params, tknots, zeros)).T
        if self.mode == 'LIN':
            spline = LinearSpline(control_points, tknots = length_params, is_cyclic = False)
        else:
            spline = CubicSpline(control_points, tknots = length_params, is_cyclic = False)
        return spline

    def solve(self, spline, input_lengths):
        spline_verts = spline.eval(input_lengths)
        return spline_verts[:,1]
    
    def calc_lengths(self, curve, tknots):
        vectors = curve.evaluate_array(tknots)
        dvs = vectors[1:] - vectors[:-1]
        lengths = np.linalg.norm(dvs, axis=1)
        return lengths

    def process(self):

        if not any((s.is_linked for s in self.outputs)):
            return

        need_eval = self.outputs['Vertices'].is_linked

        curves = self.inputs['Curve'].sv_get()
        resolution_s = self.inputs['Resolution'].sv_get()
        length_s = self.inputs['Length'].sv_get()
        samples_s = self.inputs['Samples'].sv_get(default=[[]])

        length_s = ensure_nesting_level(length_s, 2)

        ts_out = []
        verts_out = []
        for curve, resolution, input_lengths, samples, in zip_long_repeat(curves, resolution_s, length_s, samples_s):
            if self.eval_mode == 'AUTO':
                if isinstance(samples, (list, tuple)):
                    samples = samples[0]

            if isinstance(resolution, (list, tuple)):
                resolution = resolution[0]

            t_min, t_max = curve.get_u_bounds()
            tknots = np.linspace(t_min, t_max, num=resolution)
            lengths = self.calc_lengths(curve, tknots)
            length_params = np.cumsum(np.insert(lengths, 0, 0))

            if self.eval_mode == 'AUTO':
                total_length = length_params[-1]
                input_lengths = np.linspace(0.0, total_length, num = samples)
            else:
                input_lengths = np.array(input_lengths)

            spline = self.make_spline(tknots, length_params)
            ts = self.solve(spline, input_lengths).tolist()

            ts_out.append(ts)
            if need_eval:
                verts = curve.evaluate_array(ts).tolist()
                verts_out.append(verts)

        self.outputs['T'].sv_set(ts_out)
        self.outputs['Vertices'].sv_set(verts_out)

def register():
    bpy.utils.register_class(SvExCurveLengthParameterNode)

def unregister():
    bpy.utils.unregister_class(SvExCurveLengthParameterNode)
