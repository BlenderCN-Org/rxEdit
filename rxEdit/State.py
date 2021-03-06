import bpy
from bpy.types import PropertyGroup, Object
from bpy.props import BoolProperty, StringProperty, FloatVectorProperty, PointerProperty

import json

from mathutils import *
from math import *

from .bObject import *

from . import rxEdit


class State():

    def __init__(self):
        #predefine variables so i wont get confused which exist and how they are named.
        self.enabled = False
        self.cursor_location = None 
        self.main = None
        self.objects = None

    def Enabled(self, context):
        self.enabled = context.scene.rxedit.enabled
        return self.enabled

    def save(self, enabled, cursor_location, main, objects, context):
        self.enabled = enabled
        context.scene.rxedit.enabled = enabled

        self.cursor_location = cursor_location
        context.scene.rxedit.cursor_location = cursor_location.x, cursor_location.y, cursor_location.z

        self.main = main
        context.scene.rxedit.main = main.ToJson()
        
        self.objects = objects
        obj_json = []
        for obj in objects:
            obj_json.append(obj.ToJson())
        context.scene.rxedit.objects = json.dumps(obj_json)

    def clear(self, context):
        context.scene.rxedit.enabled = False
        context.scene.rxedit.cursor_location = Vector()
        context.scene.rxedit.main = ""
        context.scene.rxedit.objects = ""
    def load(self, context):
        self.enabled = context.scene.rxedit.enabled

        scene = context.scene
        self.cursor_location = Vector()
        self.cursor_location.x = scene.rxedit.cursor_location[0]
        self.cursor_location.y = scene.rxedit.cursor_location[1]
        self.cursor_location.z = scene.rxedit.cursor_location[2]

        self.main = bObject(scene.rxedit.main, context, mode=bMode.JSON)

        self.objects = []
        obj_json = json.loads(scene.rxedit.objects)
        for obj in obj_json:
            objj = json.loads(obj)
            try:
                if objj["dataname"] is not None:
                    self.objects.append(bObject(obj, context, mode=bMode.JSON))
            except Exception as ex:
                pass




class rxState(PropertyGroup):
    """rxEdit Settings"""   

    def update_wireframe(self, context):
        rxEdit.Helper.UpdateWireframeVisibility(context)

    def update_children(self, context):
        rxEdit.Helper.Update(context)
        main = rxEdit.MAIN
        for o in rxEdit.OBJECTS:
            if main.IsChild(o.Get()):
                if context.scene.rxedit.visiblechildren:
                    o.Unhide()
                else:
                    o.Hide()

    visiblechildren: BoolProperty(
        name="Visible Children",
        description="Keeps the children of the chosen object visible",
        default=True,
        update=update_children
        )
    wireframe: BoolProperty(
        name="Use Wireframe",
        description="Show a wireframe in the rxEdit mode",
        default=True,
        update=update_wireframe
        )
    wireframeobject : PointerProperty(
        name="Wireframe",
        type=Object
        )
    toggleview: BoolProperty(
        name="View Selected",
        description="View the selected object when entering mode",
        default=True
        )
    enabled : BoolProperty(
        name="Enabled",
        default=False
        )
    cursor_location : FloatVectorProperty(
        name="Cursor Location",
        description="Location of the Cursor outside of the rxEdit mode"
        )
    main : StringProperty(
        name="Main Object",
        description="Main Object"
        )
    objects : StringProperty(
        name="List of Objects in the Scene",
        description="Objects"
        )


    
def register():
    bpy.utils.register_class(rxState)
    bpy.types.Scene.rxedit = PointerProperty(type=rxState)

def unregister():
    bpy.utils.unregister_class(rxState)
    del bpy.types.Scene.rxedit

