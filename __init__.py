
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
import bl_operators

import sverchok
from sverchok.core import sv_registration_utils, make_node_list
from sverchok.utils import auto_gather_node_classes, get_node_class_reference
from sverchok.menu import SverchNodeItem, node_add_operators, SverchNodeCategory, register_node_panels, unregister_node_panels, unregister_node_add_operators
from sverchok.utils.extra_categories import register_extra_category_provider, unregister_extra_category_provider
from sverchok.ui.nodeview_space_menu import make_extra_category_menus, layout_draw_categories
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, zip_long_repeat
from sverchok.utils.logging import info, debug

# make sverchok the root module name, (if sverchok dir not named exactly "sverchok")
if __name__ != "sverchok_open3d":
    sys.modules["sverchok_open3d"] = sys.modules[__name__]

import sverchok_open3d
from sverchok_open3d import icons, settings, sockets, examples, menu
from sverchok_open3d.nodes_index import nodes_index
from sverchok_open3d.utils import show_welcome

DOCS_LINK = 'https://github.com/vicdoval/sverchok-open3d/tree/master/utils'
MODULE_NAME = 'open3d'

def make_node_list():
    modules = []
    base_name = "sverchok_open3d.nodes"
    index = nodes_index()
    for category, items in index:
        for module_name, node_name in items:
            if node_name == 'separator':
                continue
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
            menu_cats.append(cat)
    return menu_cats

def add_nodes_to_sv():
    index = nodes_index()
    for _, items in index:
        for item in items:
            nodetype = item[1]
            rna = get_node_class_reference(nodetype)
            if not rna and nodetype != 'separator':
                info("Node `%s' is not available (probably due to missing dependencies).", nodetype)
            else:
                SverchNodeItem.new(nodetype)



node_cats = plain_node_list()



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
        debug("Reloading: %s", im)
        importlib.reload(im)


def register():
    global our_menu_classes

    debug("Registering sverchok-open3d")

    settings.register()
    icons.register()
    sockets.register()

    register_nodes()
    extra_nodes = importlib.import_module(".nodes", "sverchok_open3d")
    auto_gather_node_classes(extra_nodes)

    add_nodes_to_sv()
    menu.register()

    cats_menu = make_categories() # This would load every sverchok-open3d category straight in the Sv menu

    menu_category_provider = SvO3CategoryProvider("SVERCHOK_OPEN3D", cats_menu, DOCS_LINK, use_custom_menu=True, custom_menu='NODEVIEW_MT_Open3Dx')
    register_extra_category_provider(menu_category_provider) #if 'SVERCHOK_OPEN3D' in nodeitems_utils._node_categories:
    examples.register()

    # with make_categories() This would load every sverchok-open3d category straight in the Sv menu
    # our_menu_classes = make_extra_category_menus()

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
    menu.unregister()


    icons.unregister()
    sockets.unregister()
    settings.unregister()
