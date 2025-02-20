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


bl_info = {
    "name": "Duplicate Camera with front and rear clipping swap",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0),
    "author": "Your Name",
    "description": "Duplicates selected camera, sets the new camera clipping end to be the original camera clipping start, and renames cameras. Use with alpha channel and composite in video software to create a layered 3D effect.  Use with batch render add-on to render both cameras at once."
}

import bpy

class OBJECT_OT_duplicate_camera_with_clipping(bpy.types.Operator):
    bl_idname = "object.duplicate_camera_with_clipping"
    bl_label = "Duplicate Camera with Clipping Swap"
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