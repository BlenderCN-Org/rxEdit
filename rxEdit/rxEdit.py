import bpy

from mathutils import *
from math import *

from .bObject import bObject

CURSOR_LOCATION = None
MAIN = None
OBJECTS = []

class Helper:
    def ToggleView():
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]
                bpy.ops.view3d.view_selected(ctx)
        bpy.ops.view3d.view_selected(ctx)

class BEGIN_OT_rxEdit(bpy.types.Operator):
    """Enter the rxEdit-Mode"""      
    bl_idname = "rxedit.enable"        
    bl_label = "Enter the rxEdit-Mode"         
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):        
        main = bObject(context.selected_objects[0], context)
        main.Set()

        global MAIN
        MAIN = main

        #TODO: wireframe

        #Save Cursorlocation and set it to world origin
        global CURSOR_LOCATION
        CURSOR_LOCATION = context.scene.cursor.location.copy()
        bpy.ops.view3d.snap_cursor_to_center()

        for o in context.view_layer.objects:
            obj = bObject(o, context)
            OBJECTS.append(obj)
            if not obj.EqualsSameType(main):
                obj.Hide()

        Helper.ToggleView()

        return {'FINISHED'}



class FINISH_OT_rxEdit(bpy.types.Operator):
    """Leave the rxEdit-Mode"""
    bl_idname = "rxedit.finish"
    bl_label = "Leave the rxEdit-Mode"
    bl_options = {'REGISTER'}

    def execute(self, context):        
        global MAIN
        MAIN.UpdateContext(context)
        MAIN.Unset()
        #TODO: wireframe

        #Save Cursorlocation and set it to world origin
        global CURSOR_LOCATION
        context.scene.cursor.location = CURSOR_LOCATION

        global OBJECTS
        for o in OBJECTS:
            o.Unhide()
        
        return {'FINISHED'}
        
def register():
    bpy.utils.register_class(BEGIN_OT_rxEdit)
    bpy.utils.register_class(FINISH_OT_rxEdit)

def unregister():
    bpy.utils.unregister_class(BEGIN_OT_rxEdit)
    bpy.utils.unregister_class(FINISH_OT_rxEdit)
