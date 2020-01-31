bl_info = {
    "name": "rxEdit",
    "description": "Easier editing of objects which are transformed.",
    "author": "rxc0",
    "version": (0, 4, 5),
    "blender": (2, 80, 0),
    "category": "Object"
}



import bpy
from . import rxEdit
from .rxEdit import BEGIN_OT_rxEdit, FINISH_OT_rxEdit

from . import State

addon_keymaps = []

def register():
    rxEdit.register()
    State.register()

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    km.keymap_items.new(rxEdit.BEGIN_OT_rxEdit.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=False)
    km.keymap_items.new(rxEdit.FINISH_OT_rxEdit.bl_idname, 'SPACE', 'PRESS', ctrl=False, shift=True)
    addon_keymaps.append(km)

def unregister():
    rxEdit.unregister()
    State.unregister()

    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]
