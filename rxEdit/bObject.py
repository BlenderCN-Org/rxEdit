import bpy

class bObject:
    
    def __init__(self, obj, context, ignoreScaling = True):
        self.dataname = obj.data.name
        self.location = obj.location.copy()
        self.rotation = obj.rotation_euler.copy()
        self.scale = obj.scale.copy()
        self.ignoreScale = ignoreScaling
        self.customhidden = False

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