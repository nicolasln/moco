bl_info = {
    "name": "Moco",
    "description": "Import and Export camera motion to Mark Roberts Motion Control Flair format",
    "author": "Nicolas Lemery Nantel @ Fabricated Media",
    "version": (0, 1),
    "blender": (2, 76, 0),
    "location": "View3D > Tools",
    "warning": "Only the Export functionality works at the moment",
    "wiki_url": "",
    "category": "Import-Export"}

import bpy
from datetime import datetime
from mathutils import Matrix
from math import radians

# Data Storage
class MocoData(bpy.types.PropertyGroup):
    file_import = bpy.props.StringProperty(subtype='FILE_PATH')
    file_export = bpy.props.StringProperty(subtype='FILE_PATH')
    camera = bpy.props.StringProperty()
    target = bpy.props.StringProperty()


# Import Panel
class MoCoImportPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_moco_import'
    bl_label = 'Import'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'MoCo'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        row = box.row()
        row.alignment='CENTER'
        row.label(text='Coming Soon!')


# Export Panel
class MoCoExportPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_moco_export'
    bl_label = 'Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'MoCo'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column()
        
        box = col.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text='MRMC Cartesians')
        
        col.separator()
        col.prop_search(scene.moco, 'camera', scene, 'objects', text='Camera', icon='OUTLINER_OB_CAMERA')
        col.prop_search(scene.moco, 'target', scene, 'objects', text='Target', icon='OUTLINER_OB_EMPTY')
        col.separator()
        col.prop(scene.moco, 'file_export', text='')
        col.operator('moco.export', text='Export', icon='FILE_TEXT')

# Export Operator
class MocoExport(bpy.types.Operator):
    bl_idname = 'moco.export'
    bl_label = 'Moco Export'
    bl_options = {'REGISTER'}

    def execute(self, context):
        type, message = export_mrmc_carts()
        self.report(type, message)
        return {'FINISHED'}

def export_mrmc_carts():
    """Export a camera and target to Flair MRMC Carts format.
    
    Format documentation is in the manual:
    http://www.mrmoco.com/downloads/MANUAL.pdf
    """
    scene = bpy.context.scene
    moco = bpy.context.scene.moco

    # Make sure we have a camera, target and file
    try:
        camera = scene.objects[moco.camera]
        target = scene.objects[moco.target]
    except:
        return {'ERROR'}, 'You need to select both camera and target objects'
    file_export = bpy.path.abspath(moco.file_export)
    if file_export == '':
        return {'ERROR'}, 'You need to select a file to export'

    frame_start = scene.frame_start
    frame_end = scene.frame_end
    frame_current = scene.frame_current

    # Export at frame boundaries, so there's always +1 frame
    frames = frame_end - frame_start + 1

    # Convert coordinates from Blender to MRMC
    conversion_matrix = (
        Matrix.Rotation(radians(90), 4, 'Z') *  # Rotate world 90
        Matrix.Scale(100, 4)  # Convert from Meters to Centimeters
        )

    with open(file_export, mode='w', encoding='utf-8') as file:
        file.write('# CGI Export from Blender/MoCo on {}\n'.format(
            datetime.now().strftime("%Y-%m-%d %H:%M")))
        file.write('# Exported from: {}\n'.format(bpy.data.filepath))
        file.write('# Exported objects: {}, {}\n'.format(
            scene.moco.camera, scene.moco.target))
        file.write('DATA_TYPE  CARTS_RAW  MRMC_COORDS  IN_CENTIMETRES\n')
        file.write('POINTS {}  SPEED {}\n'.format(frames, scene.render.fps))
        file.write('FRAME     XV         YV         ZV         XT         YT         ZT         ROLL')

        for frame in range(frame_start, frame_end+1):
            scene.frame_set(frame)
            v = camera.matrix_world.to_translation() * conversion_matrix
            t = target.matrix_world.to_translation() * conversion_matrix
            file.write('\n' +
                '{:4}'.format(frame) +
                '{:11.5f}'.format(v.x) +
                '{:11.5f}'.format(v.y) +
                '{:11.5f}'.format(v.z) +
                '{:11.5f}'.format(t.x) +
                '{:11.5f}'.format(t.y) +
                '{:11.5f}'.format(t.z) +
                '{:11.5f}'.format(0))  # Roll is hard-coded to 0 for now

    scene.frame_set(frame_current)
    return {'INFO'}, 'Exported {} frames to {}'.format(
        frames, bpy.path.basename(file_export))


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.moco = bpy.props.PointerProperty(type=MocoData)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.moco

if __name__ == '__main__':
    register()