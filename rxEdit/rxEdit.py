import bpy

from mathutils import *
from math import *

from .bObject import bObject
from .State import State


ENABLED = False
CURSOR_LOCATION = None
MAIN = None
OBJECTS = []
STATE = State()

class Helper:
    def Update(context):
        global ENABLED
        global MAIN
        global CURSOR_LOCATION
        global OBJECTS
        global STATE

        if not STATE.Enabled(context):
            ENABLED = False
            return

        STATE.load(context)
        ENABLED = STATE.enabled
        MAIN = STATE.main
        CURSOR_LOCATION = STATE.cursor_location
        OBJECTS = STATE.objects

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
        Helper.Update(context)

        global ENABLED
        if ENABLED:
            self.report({'INFO'}, "Already in rxEdit mode!")
            return {'FINISHED'}

        main = bObject(context.selected_objects[0], context)
        main.Set()
        
        #TODO: wireframe

        #Save Cursor's location and set it to world origin
        cursor_location = context.scene.cursor.location.copy()
        bpy.ops.view3d.snap_cursor_to_center()

        objcts = []
        for o in context.view_layer.objects:
            obj = bObject(o, context)
            objcts.append(obj)
            if not obj.EqualsSameType(main):
                obj.Hide()

        Helper.ToggleView()
       
        global STATE
        STATE.save(True, cursor_location, main, objcts, context)

        return {'FINISHED'}



class FINISH_OT_rxEdit(bpy.types.Operator):
    """Leave the rxEdit-Mode"""
    bl_idname = "rxedit.finish"
    bl_label = "Leave the rxEdit-Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):       
        Helper.Update(context)
        
        global ENABLED
        if not ENABLED:
            return {'FINISHED'}
            
        MAIN.Unset()
        #TODO: wireframe

        #Save Cursorlocation and set it to world origin
        global CURSOR_LOCATION
        context.scene.cursor.location = CURSOR_LOCATION

        global OBJECTS
        for o in OBJECTS:
            o.Unhide()
        

        global STATE
        STATE.clear(context)

        return {'FINISHED'}
        
def register():
    bpy.utils.register_class(BEGIN_OT_rxEdit)
    bpy.utils.register_class(FINISH_OT_rxEdit)

def unregister():
    bpy.utils.unregister_class(BEGIN_OT_rxEdit)
    bpy.utils.unregister_class(FINISH_OT_rxEdit)
