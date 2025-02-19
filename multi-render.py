bl_info = {
    "name": "Render from Multiple Selected Cameras",
    "blender": (3, 0, 0),
    "category": "Render",
    "version": (1, 0),
    "author": "Your Name",
    "description": "Renders all frames of the current scene from each selected camera, saving files with camera names.",
}

import bpy
import os

class RENDER_OT_render_from_selected_cameras(bpy.types.Operator):
    bl_idname = "render.render_from_selected_cameras"
    bl_label = "Render from Selected Cameras"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Ensure at least one camera is selected
        return any(obj.type == 'CAMERA' for obj in context.selected_objects)

    def execute(self, context):
        # Get the output folder from the render settings
        output_path = bpy.context.scene.render.filepath
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Store the original active camera
        original_camera = context.scene.camera

        # Loop through all selected objects
        for obj in context.selected_objects:
            if obj.type == 'CAMERA':
                # Set the current camera as the active camera
                context.scene.camera = obj

                # Set the output file path to include the camera name
                camera_name = obj.name
                context.scene.render.filepath = os.path.join(output_path, f"render_{camera_name}_")

                # Render the animation
                bpy.ops.render.render(animation=True)

                self.report({'INFO'}, f"Rendered animation from camera: {camera_name}")

        # Restore the original active camera and filepath
        context.scene.camera = original_camera
        context.scene.render.filepath = output_path

        self.report({'INFO'}, "Rendering completed for all selected cameras.")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(RENDER_OT_render_from_selected_cameras.bl_idname)

def register():
    bpy.utils.register_class(RENDER_OT_render_from_selected_cameras)
    bpy.types.TOPBAR_MT_render.append(menu_func)

def unregister():
    bpy.utils.unregister_class(RENDER_OT_render_from_selected_cameras)
    bpy.types.TOPBAR_MT_render.remove(menu_func)

if __name__ == "__main__":
    register()
    