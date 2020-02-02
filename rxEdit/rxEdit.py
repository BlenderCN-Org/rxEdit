import bpy
import bpy
from bpy.types import Operator

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

    def UpdateWireframeVisibility(context):
        Helper.Update(context)
        global ENABLED
        if not ENABLED:
            return
        wireframe = context.scene.rxedit.wireframeobject
        wireframe.hide_viewport = not context.scene.rxedit.wireframe


class TOGGLE_OT_rxEdit(Operator):
    """Toggle rxEdit-Mode"""      
    bl_idname = "rxedit.toggle"        
    bl_label = "Toggle rxEdit-Mode"         
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):     
        Helper.Update(context)
        global ENABLED
        if ENABLED:
            bpy.ops.rxedit.finish('EXEC_DEFAULT')
        else:
            bpy.ops.rxedit.enable('EXEC_DEFAULT')
        return {'FINISHED'}


class BEGIN_OT_rxEdit(Operator):
    """Enter the rxEdit-Mode"""      
    bl_idname = "rxedit.enable"        
    bl_label = "Enter the rxEdit-Mode"         
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):     
        Helper.Update(context)

        global ENABLED
        if ENABLED:
            self.report({'WARNING'}, "Already in rxEdit mode!")
            return {'FINISHED'}

        main = bObject(context.object, context)
        main.Set()
        
        #Create wireframe
        wireframe = bpy.data.objects.new('rxWIREFRAME', context.object.data)
        wireframe.scale = context.object.scale.copy()
        wireframe.display_type = 'WIRE'
        wireframe.hide_select = True
        context.object.users_collection[0].objects.link(wireframe)
        context.scene.rxedit.wireframeobject = wireframe
        Helper.UpdateWireframeVisibility(context)

        #Save Cursor's location and set it to world origin
        cursor_location = context.scene.cursor.location.copy()
        bpy.ops.view3d.snap_cursor_to_center()

        objcts = []
        for o in context.view_layer.objects:
            obj = bObject(o, context)
            objcts.append(obj)
            if context.scene.rxedit.visiblechildren and main.IsChild(o):
                continue
            if not main.Equals(o):
                obj.Hide()
        if context.scene.rxedit.toggleview:
            Helper.ToggleView()
       
        global STATE
        STATE.save(True, cursor_location, main, objcts, context)

        return {'FINISHED'}

class FINISH_OT_rxEdit(Operator):
    """Leave the rxEdit-Mode"""
    bl_idname = "rxedit.finish"
    bl_label = "Leave the rxEdit-Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):       
        Helper.Update(context)
        
        global ENABLED
        if not ENABLED:
            return {'FINISHED'}
            

        #detecting new created objects
        global OBJECTS
        new_objects = context.view_layer.objects
        for o in OBJECTS:
            o.Unhide()
            new_objects = [obj for obj in new_objects if obj.data.name != o.dataname]

        global MAIN

        #parent them (see issue #4)
        mainobj = MAIN.Get()
        for new in new_objects:
            if new.parent is None:
                new.parent = mainobj
        
        MAIN.Unset()

        #moving them with the object and unparenting them(see issue #4)
        bpy.context.view_layer.update()
        for new in new_objects:
            if MAIN.IsChild(new):
                new_wm = new.matrix_world.copy() 
                new.parent = None
                new.matrix_world = new_wm

        #Delete wireframe
        wireframe = context.scene.rxedit.wireframeobject
        bpy.ops.object.select_all(action='DESELECT')
        wireframe.hide_select = False
        wireframe.hide_viewport = False
        wireframe.select_set(True)
        bpy.ops.object.delete()
        context.scene.rxedit.wireframeobject = None

        mainobj.select_set(True)

        #Set the Cursorlocation back to where it was
        global CURSOR_LOCATION
        context.scene.cursor.location = CURSOR_LOCATION    

        global STATE
        STATE.clear(context)

        return {'FINISHED'}
        
def register():
    bpy.utils.register_class(TOGGLE_OT_rxEdit)
    bpy.utils.register_class(BEGIN_OT_rxEdit)
    bpy.utils.register_class(FINISH_OT_rxEdit)

def unregister():
    bpy.utils.unregister_class(TOGGLE_OT_rxEdit)
    bpy.utils.unregister_class(BEGIN_OT_rxEdit)
    bpy.utils.unregister_class(FINISH_OT_rxEdit)
