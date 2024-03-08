
bl_info = {
    "name": "Sverchok-Open3d",
    "author": "Victor Doval",
    "version": (0, 1, 0, 0),
    "blender": (2, 81, 0),
    "location": "Node Editor",
    "category": "Node",
    "description": "Sverchok Open 3d",
    "warning": "",
    "wiki_url": "https://github.com/vicdoval/sverchok-open3d",
    "tracker_url": "https://github.com/vicdoval/sverchok-open3d/issues"
}

import sys
import importlib
from pathlib import Path
import nodeitems_utils

import sverchok
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat
from sverchok.utils.context_managers import sv_preferences
from sverchok.utils.sv_logging import sv_logger
from sverchok.ui.nodeview_space_menu import add_node_menu, Category

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != "sverchok_open3d":
    sys.modules["sverchok_open3d"] = sys.modules[__name__]

import sverchok_open3d
from sverchok_open3d import icons
from sverchok_open3d import settings
from sverchok_open3d import sockets
from sverchok_open3d.nodes_index import nodes_index
from sverchok_open3d.utils import show_welcome

DOCS_LINK = 'https://github.com/vicdoval/sverchok-open3d/tree/master/utils'
MODULE_NAME = 'open3d'

# Convert struct to menu.
# In:
#   - source struct
#   - lambda to convert tuples (final items are tuples in format ("{path}utils.o3d_import", "{class_name}SvO3ImportNode"))
def convert_config(obj, func=None):
    if not func:
        func = lambda elem: elem # call only on tuples
    cls_names = []
    if type(obj)==dict:
        cls_names = dict()

    for elem in obj:
        if elem==None: # this is menu items break
            cls_names.append( func(elem) )
        elif type(elem)==tuple:
            cls_names.append( func(elem) ) # this is menu item - tuple of two params
        elif type(obj)==dict:
            res = convert_config(obj[elem], func) # this is submenu
            if res:
                cls_names[elem]=res
        elif type(obj)==list:
            res = convert_config(elem, func)
            if res:
                cls_names.append(res)
        else:
            raise Exception("Menu struct error")
    return cls_names

# function as argument for convert_config. call only on tuples
def collect_classes_names(elem):
    if elem is None:
        res = '---'  # menu splitter. Used by Sverchok.
    elif isinstance(elem[0], dict): # property of menugroup, ex: ({'icon_name': 'MESH_BOX'}) for icon.
        res = elem[0]
    else:
        res = elem[1]  # class name to bind to menu Shift-A
    return res
nodes_items = convert_config(nodes_index(), collect_classes_names)
add_node_menu.append_from_config( nodes_items )

def make_node_list():
    modules = []
    base_name = "sverchok_open3d.nodes"
    arr_items = []
    def collect_module_names(elem):
        if elem is not None:
            if isinstance(elem[0], str):
                arr_items.append(elem[0])
        return elem
    convert_config(nodes_index(), collect_module_names)
    for module_name in arr_items:
        module = importlib.import_module(f".{module_name}", base_name)
        modules.append(module)
    return modules

imported_modules = [icons] + make_node_list()

reload_event = False

if "bpy" in locals():
    reload_event = True
    sv_logger.info("Reloading sverchok-open3d...")

import bpy

def register_nodes():
    node_modules = make_node_list()
    for module in node_modules:
        module.register()
    sv_logger.info("Registered %s nodes", len(node_modules))

def unregister_nodes():
    global imported_modules
    for module in reversed(imported_modules):
        module.unregister()

our_menu_classes = []

def reload_modules():
    global imported_modules
    for im in imported_modules:
        sv_logger.debug("Reloading: %s", im)
        importlib.reload(im)


def register():
    global our_menu_classes

    sv_logger.debug("Registering sverchok-open3d")

    add_node_menu.register()
    settings.register()
    icons.register()
    sockets.register()

    register_nodes()
    #extra_nodes = importlib.import_module(".nodes", "sverchok_open3d")
    show_welcome()

def unregister():
    global our_menu_classes
    if 'SVERCHOK_OPEN3D' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVERCHOK_OPEN3D")
    for clazz in our_menu_classes:
        try:
            bpy.utils.unregister_class(clazz)
        except Exception as e:
            print("Can't unregister menu class %s" % clazz)
            print(e)
    unregister_nodes()

    sockets.unregister()
    icons.unregister()
    settings.unregister()
    #add_node_menu.unregister() - do not unregister!!! See sverchok\ui\nodeview_space_menu.py module's comments 
