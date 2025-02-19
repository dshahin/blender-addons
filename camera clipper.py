bl_info = {
    "name": "Duplicate Camera with Clipping",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0),
    "author": "Your Name",
    "description": "Duplicates a camera, sets clipping distances, and renames cameras.",
}

import bpy

class OBJECT_OT_duplicate_camera_with_clipping(bpy.types.Operator):
    bl_idname = "object.duplicate_camera_with_clipping"
    bl_label = "Duplicate Camera with Clipping"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'CAMERA'

    def execute(self, context):
        original_camera = context.object

        # Store the original camera's clip_start value
        original_clip_start = original_camera.data.clip_start

        # Duplicate the camera
        bpy.ops.object.duplicate()
        new_camera = context.object

        # Set the clipping distances for the new camera
        new_camera.data.clip_start = 0.01  # Set clip_start to 0
        new_camera.data.clip_end = original_clip_start  # Set clip_end to the original camera's clip_start

        # Rename the cameras
        original_camera.name = "camera.rear"
        new_camera.name = "camera.front"

        bpy.context.scene.camera = new_camera

        self.report({'INFO'}, f"Duplicated camera: 'camera.front' and 'camera.rear' created with adjusted clipping distances.")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_duplicate_camera_with_clipping.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_duplicate_camera_with_clipping)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_duplicate_camera_with_clipping)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()