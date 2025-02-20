import bpy
import os
from bpy.app.handlers import persistent

bl_info = {
    "name": "Batch Render Selected Cameras",
    "blender": (3, 0, 0),
    "category": "Render",
    "description": "Render animations from all selected cameras with filenames including camera names.",
}

# Global variables to track rendering progress
render_queue = []
current_camera = None
original_camera = None
original_filepath = None

class BatchRenderCameras(bpy.types.Operator):
    bl_idname = "render.batch_render_cameras"
    bl_label = "Batch Render Selected Cameras"
    bl_description = "Render animations from all selected cameras"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global render_queue, current_camera, original_camera, original_filepath

        scene = context.scene
        selected_cameras = [obj for obj in context.selected_objects if obj.type == 'CAMERA']

        if not selected_cameras:
            self.report({'WARNING'}, "No cameras selected!")
            return {'CANCELLED'}

        # Store the original camera and filepath
        original_camera = scene.camera
        original_filepath = scene.render.filepath

        # Get the output directory from the scene's render settings
        output_dir = bpy.path.abspath(scene.render.filepath)

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create a queue of cameras to render
        render_queue = []
        for camera in selected_cameras:
            filename = f"{camera.name}.mp4"
            filepath = os.path.join(output_dir, filename)
            render_queue.append((camera, filepath))

        # Start the modal operator
        context.window_manager.modal_handler_add(self)
        self._start_next_render(context)

        return {'RUNNING_MODAL'}

    def _start_next_render(self, context):
        global render_queue, current_camera

        if render_queue:
            current_camera, filepath = render_queue.pop(0)
            context.scene.camera = current_camera
            context.scene.render.filepath = filepath

            # Start rendering
            bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
        else:
            self._finish_rendering(context)

    def _finish_rendering(self, context):
        global original_camera, original_filepath

        # Restore the original camera and filepath
        context.scene.camera = original_camera
        context.scene.render.filepath = original_filepath

        # Reset global variables
        original_camera = None
        original_filepath = None

        self.report({'INFO'}, "Batch rendering complete!")
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'ESC':
            self._finish_rendering(context)
            return {'CANCELLED'}

        # Check if the current render is finished
        if not bpy.app.is_job_running('RENDER'):
            self._start_next_render(context)

        return {'PASS_THROUGH'}

def menu_func(self, context):
    self.layout.operator(BatchRenderCameras.bl_idname, icon='RENDER_ANIMATION')

def register():
    bpy.utils.register_class(BatchRenderCameras)
    bpy.types.TOPBAR_MT_render.append(menu_func)

def unregister():
    bpy.utils.unregister_class(BatchRenderCameras)
    bpy.types.TOPBAR_MT_render.remove(menu_func)

if __name__ == "__main__":
    register()