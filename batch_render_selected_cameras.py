# MIT License

# Copyright (c) 2025 Dan Shahin

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import bpy
import os
from bpy.app.handlers import persistent

bl_info = {
    "name": "Batch Render Selected Cameras",
    "blender": (3, 0, 0),
    "category": "Render",
    "description": "This Blender add-on allows users to batch render animations from multiple selected cameras. It provides a user interface in Blender's render menu and handles rendering each camera's animation sequentially. It also includes error handling and user feedback through the UI.",
}

# Global variables to track rendering progress
render_queue = []
current_camera = None
original_camera = None
original_filepath = None
original_frame_start = None
original_frame_end = None

class BatchRenderCameras(bpy.types.Operator):
    bl_idname = "render.batch_render_cameras"
    bl_label = "Batch Render Selected Cameras"
    bl_description = "Render animations from all selected cameras with custom frame ranges"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global render_queue, current_camera, original_camera, original_filepath, original_frame_start, original_frame_end

        scene = context.scene
        selected_cameras = [obj for obj in context.selected_objects if obj.type == 'CAMERA']

        if not selected_cameras:
            self.report({'WARNING'}, "No cameras selected!")
            return {'CANCELLED'}

        # Store the original camera, filepath, and frame range
        original_camera = scene.camera
        original_filepath = scene.render.filepath
        original_frame_start = scene.frame_start
        original_frame_end = scene.frame_end

        # Get the output directory from the scene's render settings
        output_dir = bpy.path.abspath(scene.render.filepath)

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Add custom properties to selected cameras if they don't exist
        for camera in selected_cameras:
            if "frame_start" not in camera:
                camera["frame_start"] = scene.frame_start
            if "frame_end" not in camera:
                camera["frame_end"] = scene.frame_end

        # Create a queue of cameras to render, with custom frame ranges
        render_queue = []
        for camera in selected_cameras:
            frame_start = camera["frame_start"]
            frame_end = camera["frame_end"]

            filename = f"{camera.name}.mp4"
            filepath = os.path.join(output_dir, filename)
            render_queue.append((camera, filepath, frame_start, frame_end))

        # Start the modal operator
        context.window_manager.modal_handler_add(self)
        self._start_next_render(context)

        return {'RUNNING_MODAL'}

    def _start_next_render(self, context):
        global render_queue, current_camera

        if render_queue:
            current_camera, filepath, frame_start, frame_end = render_queue.pop(0)
            context.scene.camera = current_camera
            context.scene.render.filepath = filepath

            # Set the custom frame range for this camera
            context.scene.frame_start = frame_start
            context.scene.frame_end = frame_end

            # Start rendering
            bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
        else:
            self._finish_rendering(context)

    def _finish_rendering(self, context):
        global original_camera, original_filepath, original_frame_start, original_frame_end

        # Restore the original camera, filepath, and frame range
        context.scene.camera = original_camera
        context.scene.render.filepath = original_filepath
        context.scene.frame_start = original_frame_start
        context.scene.frame_end = original_frame_end

        # Reset global variables
        original_camera = None
        original_filepath = None
        original_frame_start = None
        original_frame_end = None

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