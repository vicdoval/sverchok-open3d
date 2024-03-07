
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
from sverchok.utils.sv_logging import sv_logger
from sverchok.ui.nodeview_space_menu import add_node_menu

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

def convert_config(config):
    new_form = []
    for cat_name, items in config:
        new_items = []
        for item in items:
            if item is None:
                new_items.append('---')
                continue
            path, bl_idname = item
            new_items.append(bl_idname)
        cat = {cat_name: new_items}
        new_form.append(cat)
    return new_form

add_node_menu.append_from_config(convert_config(nodes_index()))

def make_node_list():
    modules = []
    base_name = "sverchok_open3d.nodes"
    index = nodes_index()
    for category, items in index:
        for item in items:
            if not item:
                continue
            module_name, node_name = item
            module = importlib.import_module(f".{module_name}", base_name)
            modules.append(module)
    return modules

def plain_node_list():
    node_cats = {}
    index = nodes_index()
    for category, items in index:
        nodes = []
        for _, node_name in items:
            nodes.append([node_name])
        node_cats[category] = nodes
    return node_cats
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

def make_categories():
    menu_cats = []
    index = nodes_index()
    for category, items in index:
        identifier = "SVERCHOK_OPEN3D_" + category.replace(' ', '_')
        node_items = []
        for item in items:
            nodetype = item[1]
            rna = get_node_class_reference(nodetype)
            if not rna and nodetype != 'separator':
                sv_logger.info("Node `%s' is not available (probably due to missing dependencies).", nodetype)
            else:
                node_item = SverchNodeItem.new(nodetype)
                node_items.append(node_item)
        if node_items:
            cat = SverchNodeCategory(
                        identifier,
                        category,
                        items=node_items
                    )
            menu_cats.append(cat)
    return menu_cats

def add_nodes_to_sv():
    index = nodes_index()
    for _, items in index:
        for item in items:
            nodetype = item[1]
            rna = get_node_class_reference(nodetype)
            if not rna and nodetype != 'separator':
                sv_logger.info("Node `%s' is not available (probably due to missing dependencies).", nodetype)
            else:
                SverchNodeItem.new(nodetype)

class SvO3CategoryProvider(object):
    def __init__(self, identifier, cats_menu, docs_link, use_custom_menu=False, custom_menu=None):
        self.identifier = identifier
        self.menu = cats_menu
        self.docs = docs_link
        self.use_custom_menu = use_custom_menu
        self.custom_menu = custom_menu

    def get_categories(self):
        return self.menu

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
    extra_nodes = importlib.import_module(".nodes", "sverchok_open3d")
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
    unregister_nodes()

    sockets.unregister()
    icons.unregister()
    settings.unregister()
    #add_node_menu.unregister() - do not unregister!!! See sverchok\ui\nodeview_space_menu.py module's comments 
