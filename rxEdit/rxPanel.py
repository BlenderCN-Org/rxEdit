import bpy
from bpy.types import Panel
from bpy.props import BoolProperty, StringProperty, FloatVectorProperty, PointerProperty

from .rxEdit import BEGIN_OT_rxEdit, FINISH_OT_rxEdit

class OPTIONS_PT_rxEdit(Panel):
    bl_label = "rxEdit Options"
    bl_category = "rxEdit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()  
        col.label(text="Options")
        row.prop(context.scene.rxedit, "toggleview", icon='HIDE_OFF',icon_only=True)
        row.prop(context.scene.rxedit, "visiblechildren", icon='MONKEY',icon_only=True)
        row.prop(context.scene.rxedit, "wireframe", icon='MOD_WIREFRAME', icon_only=True)

        layout.separator()
        row = layout.row()
        row.operator(operator="rxedit.toggle", text="Toggle rxEdit-Mode")

        
def register():
    bpy.utils.register_class(OPTIONS_PT_rxEdit)

def unregister():
    bpy.utils.unregister_class(OPTIONS_PT_rxEdit)