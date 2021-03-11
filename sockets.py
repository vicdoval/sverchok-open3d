
import os
import glob
import bpy
from bpy.types import NodeSocket
from sverchok.core.sockets import SvSocketCommon
from sverchok.data_structure import (
    enum_item_4,
    get_other_socket, replace_socket,
    SIMPLE_DATA_TYPES,
    flatten_data, graft_data, map_at_level, wrap_data, unwrap_data)
from sverchok_open3d.dependencies import open3d as o3d
if o3d is not None:
    TriangleMesh = o3d.cpu.pybind.geometry.TriangleMesh
    PointCloud = o3d.cpu.pybind.geometry.PointCloud
else:
    TriangleMesh = None
    PointCloud = None
class SvO3PointCloudSocket(NodeSocket, SvSocketCommon):
    '''For Opend 3d Point Cloud data'''
    bl_idname = "SvO3PointCloudSocket"
    bl_label = "Opend3d Point Cloud Socket"
    nesting_level: bpy.props.IntProperty(default=1)
    color = (0.9583199126725049, 0.8853214990457389, 0.5110029362033784, 1.0)
    def do_flatten(self, data):
        return flatten_data(data, 1, data_types=(PointCloud,))

    def do_graft(self, data):
        return graft_data(data, item_level=0, data_types=(PointCloud,))

class SvO3TriangleMeshSocket(NodeSocket, SvSocketCommon):
    '''For Opend 3d Triangle Mesh data'''
    bl_idname = "SvO3TriangleMeshSocket"
    bl_label = "Opend3d Triangle Mesh Socket"
    nesting_level: bpy.props.IntProperty(default=1)
    color = (0.7932965189126601, 0.6152367870411551, 0.8604365081694361, 1.0)
    def do_flatten(self, data):
        return flatten_data(data, 1, data_types=(TriangleMesh,))

    def do_graft(self, data):
        return graft_data(data, item_level=0, data_types=(TriangleMesh,))

classes = [
    SvO3PointCloudSocket, SvO3TriangleMeshSocket
]
register, unregister = bpy.utils.register_classes_factory(classes)
