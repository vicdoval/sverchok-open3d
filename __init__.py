
bl_info = {
    "name": "Sverchok-Open3d",
    "author": "Victor Doval",
    "version": (0, 1, 0, 0),
    "blender": (2, 81, 0),
    "location": "Node Editor",
    "category": "Node",
    "description": "Sverchok Open 3d",
    "warning": "",
    "wiki_url": "http://nikitron.cc.ua/sverch/html/main.html",
    "tracker_url": "http://www.blenderartists.org/forum/showthread.php?272679"
}

import sys
import importlib

import nodeitems_utils
import bl_operators

import sverchok
from sverchok.core import sv_registration_utils, make_node_list
from sverchok.utils import auto_gather_node_classes, get_node_class_reference
from sverchok.menu import SverchNodeItem, node_add_operators, SverchNodeCategory, register_node_panels, unregister_node_panels, unregister_node_add_operators
from sverchok.utils.extra_categories import register_extra_category_provider, unregister_extra_category_provider
from sverchok.ui.nodeview_space_menu import make_extra_category_menus
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat
from sverchok.utils.logging import info, debug

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != "sverchok_open3d":
    sys.modules["sverchok_open3d"] = sys.modules[__name__]

from sverchok_open3d import icons
from sverchok_open3d import settings
from sverchok_open3d.utils import show_welcome

def nodes_index():
    return [("Open 3D", [
                ("point_cloud.point_cloud_in", "SvO3PointCloudImportNode"),
                ("point_cloud.point_cloud_import", "SvO3PointCloudInNode"),
                ("point_cloud.point_cloud_out", "SvO3PointCloudOutNode"),
                ("point_cloud.mesh_from_point_cloud", "SvO3MeshFrom3PointCloudNode"),
                ("point_cloud.point_cloud_export", "SvO3PointCloudExportNode"),
            ]),
            # ("Extra Curves", [
            #     ("curve.intersect_surface_plane", "SvExCrossSurfacePlaneNode"),
            #     ("curve.fourier_curve", "SvFourierCurveNode"),
            #     ("curve.approximate_fourier_curve", "SvApproxFourierCurveNode"),
            #     ("curve.interpolate_fourier_curve", "SvInterpFourierCurveNode")
            # ]),
            # ("Extra Fields", [
            #     ("field.vfield_lines_on_surface", "SvExVFieldLinesOnSurfNode")
            # ]),
            # ("Extra Solids", [
            #     ("solid.solid_waffle", "SvSolidWaffleNode")
            # ]),
            # ("Extra Spatial", [
            #     ("spatial.delaunay3d_surface", "SvDelaunayOnSurfaceNode"),
            #     ("spatial.delaunay_mesh", "SvDelaunayOnMeshNode")
            # ]),
            # ("Data", [
            #     ("data.spreadsheet", "SvSpreadsheetNode"),
            #     ("data.data_item", "SvDataItemNode")
            # ])
    ]

def make_node_list():
    modules = []
    base_name = "sverchok_open3d.nodes"
    index = nodes_index()
    for category, items in index:
        for module_name, node_name in items:
            module = importlib.import_module(f".{module_name}", base_name)
            modules.append(module)
    return modules

imported_modules = [icons] + make_node_list()

reload_event = False

if "bpy" in locals():
    reload_event = True
    info("Reloading sverchok-open3d...")
    reload_modules()

import bpy

def register_nodes():
    node_modules = make_node_list()
    for module in node_modules:
        module.register()
    info("Registered %s nodes", len(node_modules))

def unregister_nodes():
    global imported_modules
    for module in reversed(imported_modules):
        module.unregister()

def make_menu():
    menu = []
    index = nodes_index()
    for category, items in index:
        identifier = "SVERCHOK_OPEN3D_" + category.replace(' ', '_')
        node_items = []
        for item in items:
            nodetype = item[1]
            rna = get_node_class_reference(nodetype)
            if not rna:
                info("Node `%s' is not available (probably due to missing dependencies).", nodetype)
            else:
                node_item = SverchNodeItem.new(nodetype)
                node_items.append(node_item)
        if node_items:
            cat = SverchNodeCategory(
                        identifier,
                        category,
                        items=node_items
                    )
            menu.append(cat)
    return menu

class SvExCategoryProvider(object):
    def __init__(self, identifier, menu):
        self.identifier = identifier
        self.menu = menu

    def get_categories(self):
        return self.menu

our_menu_classes = []

def reload_modules():
    global imported_modules
    for im in imported_modules:
        debug("Reloading: %s", im)
        importlib.reload(im)

def register():
    global our_menu_classes

    debug("Registering sverchok-open3d")

    settings.register()
    icons.register()

    register_nodes()
    extra_nodes = importlib.import_module(".nodes", "sverchok_open3d")
    auto_gather_node_classes(extra_nodes)
    menu = make_menu()
    menu_category_provider = SvExCategoryProvider("SVERCHOK_OPEN3D", menu)
    register_extra_category_provider(menu_category_provider) #if 'SVERCHOK_OPEN3D' in nodeitems_utils._node_categories:
        #unregister_node_panels()
        #nodeitems_utils.unregister_node_categories("SVERCHOK_OPEN3D")

    our_menu_classes = make_extra_category_menus()
    #register_node_panels("SVERCHOK_OPEN3D", menu)
    show_welcome()

def unregister():
    global our_menu_classes
    if 'SVERCHOK_OPEN3D' in nodeitems_utils._node_categories:
        #unregister_node_panels()
        nodeitems_utils.unregister_node_categories("SVERCHOK_OPEN3D")
    for clazz in our_menu_classes:
        try:
            bpy.utils.unregister_class(clazz)
        except Exception as e:
            print("Can't unregister menu class %s" % clazz)
            print(e)
    unregister_extra_category_provider("SVERCHOK_OPEN3D")
    #unregister_node_add_operators()
    unregister_nodes()

    icons.unregister()
    settings.unregister()
