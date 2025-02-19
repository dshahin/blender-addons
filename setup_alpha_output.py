
bl_info = {
    "name": "Setup Scene with Alpha Quicktime",
    "author": "Dan Shahin",
    "version": (1, 2),
    "blender": (2, 93, 1),
    "location": "Output Menu",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy


def main(context):
    # setup defaults
    bpy.context.scene.render.resolution_x = 1280
    bpy.context.scene.render.resolution_y = 720

    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'

    bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'
    bpy.context.scene.render.ffmpeg.codec = 'QTRLE'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.eevee.use_gtao = True
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.engine = 'CYCLES'
    
    cam = bpy.context.scene.camera
    filepath = "/Users/danielshahin/Pictures/backgrounds/neighborhood of make believe set.png"

    img = bpy.data.images.load(filepath)
    cam.data.show_background_images = True
    
    
    bg = cam.data.background_images.new()
    bg.image = img
    
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.transform.resize(value=(18.7869, 18.7869, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
    cam.data.background_images[0].display_depth = 'FRONT'

    shadow_catcher = bpy.context.active_object
    shadow_catcher.cycles.is_shadow_catcher = True
    shadow_catcher.update_tag()


class SetupOutput(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "shahin.setup_output"
    bl_label = "Setup Output"



    def execute(self, context):
        main(context)
        return {'FINISHED'}


class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        
        # Big render button
        layout.label(text="Alpha Setup")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("shahin.setup_output")
        
        # Big render button
        layout.label(text="Render:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")

       

def register():
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(SetupOutput)


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(SetupOutput)


if __name__ == "__main__":
    register()
