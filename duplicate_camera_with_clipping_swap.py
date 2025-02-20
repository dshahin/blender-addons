bl_info = {
    "name": "Duplicate Camera with front and rear Clipping",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0),
    "author": "Your Name",
    "description": "Duplicates a camera, sets clipping distances, and renames cameras. Activated via Outliner right-click.",
}

import bpy

class OBJECT_OT_duplicate_camera_with_clipping(bpy.types.Operator):
    bl_idname = "object.duplicate_camera_with_clipping"
    bl_label = "Duplicate Camera with Clipping"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Ensure the active object is a camera
        return context.object and context.object.type == 'CAMERA'

    def execute(self, context):
        original_camera = context.object

        # Store the original camera's clip_start value
        original_clip_start = original_camera.data.clip_start

        # Duplicate the camera
        bpy.ops.object.duplicate()
        new_camera = context.object

        # Set the clipping distances for the new camera
        new_camera.data.clip_start = 0.01  # Set clip_start to 0.01
        new_camera.data.clip_end = original_clip_start  # Set clip_end to the original camera's clip_start

        # Rename the cameras
        original_camera.name = "camera.rear"
        new_camera.name = "camera.front"

        # Set the new camera as the active camera
        bpy.context.scene.camera = new_camera


        self.report({'INFO'}, f"Duplicated camera: 'camera.front' and 'camera.rear' created with adjusted clipping distances.")
        return {'FINISHED'}

# Add the operator to the Outliner's context menu
def outliner_menu_func(self, context):
    # Check if the selected object is a camera
    if context.selected_objects and context.selected_objects[0].type == 'CAMERA':
        self.layout.operator(OBJECT_OT_duplicate_camera_with_clipping.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_duplicate_camera_with_clipping)
    bpy.types.OUTLINER_MT_context_menu.append(outliner_menu_func)  # Add to the Outliner's right-click context menu

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_duplicate_camera_with_clipping)
    bpy.types.OUTLINER_MT_context_menu.remove(outliner_menu_func)  # Remove from the Outliner's right-click context menu

if __name__ == "__main__":
    register()