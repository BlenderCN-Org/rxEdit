import bpy
import json
from mathutils import *
from math import *
from enum import Enum

class bMode(Enum):
    OBJECT = 0,
    JSON = 1

class bObject:
    
    def __init__(self, obj, context, ignoreScaling = True, mode = bMode.OBJECT):
        self.context = context
        if mode == bMode.OBJECT: #obj is probably a blender object
            self.dataname = obj.data.name
            self.location = obj.location.copy()
            self.rotation = obj.rotation_euler.copy()
            self.scale = obj.scale.copy()
            self.ignoreScale = ignoreScaling
            self.customhidden = False
        else: # obj is probably a json string
            obj = json.loads(obj)
            self.dataname = obj["dataname"]
            self.location = self.JsonVector(Vector(), obj["location"])
            self.rotation = self.JsonVector(Euler(), obj["rotation"])
            self.scale = self.JsonVector(Vector(), obj["scale"])
            self.ignoreScale = obj["ignoreScale"]
            self.customhidden = obj["customhidden"]


        self.context = context

    def Hide(self):
        myself = self.Get()
        if not myself.hide_viewport and myself.visible_get():
            myself.hide_viewport = True
            self.customhidden = True

    def Unhide(self):
        myself = self.Get()
        myself.hide_viewport = False    

    def UpdateContext(self, context):
        self.context = context

    def Get(self):
        for obj in self.context.view_layer.objects:
            if obj.data.name == self.dataname:
                return obj
        return None

    def Set(self):
        myself = self.Get()
        myself.select_set(True)

        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()

    def Unset(self):
        myself = self.Get()
        myself.location = self.location
        myself.rotation_euler = self.rotation
        if self.ignoreScale:
            myself.scale = self.scale

    def IsChild(self, object):
        myself = self.Get()
        return object.parent is not None and object.parent.data.name == self.dataname

    def Equals(self, obj):
        return self.dataname == obj.data.name

    def EqualsSameType(self, obj):
        return self.dataname == obj.dataname

    def VectorJson(self, vector):
        data = {"x": vector.x,
                "y": vector.y,
                "z": vector.z}
        return data

    def JsonVector(self, vector, json):
        vector.x = json["x"]
        vector.y = json["y"]
        vector.z = json["z"]
        return vector

    def ToJson(self):

        data = {"dataname": self.dataname,
                "location": self.VectorJson(self.location),
                "rotation": self.VectorJson(self.rotation),
                "scale": self.VectorJson(self.scale),
                "ignoreScale": self.ignoreScale,
                "customhidden": self.customhidden}

        return json.dumps(data)

