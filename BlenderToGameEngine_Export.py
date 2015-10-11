bl_info = {
    "name": "Blender to Game Object Export",
    "category": "Import-Export",
}

import bpy
import os
from mathutils import Vector

# plugin
class GameExport(bpy.types.Panel):
    bl_label = "Game Engine Export"
    bl_idname = "OBJECT_PT_UnityExport"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    
    #scene vars
    bpy.types.Scene.file_dir = bpy.props.StringProperty(name = "File Directory",description="Where the file will be save to.")
    bpy.types.Scene.file_name = bpy.props.StringProperty(name = "File Name",description="name of the file. Example Main_Character")
    bpy.types.Scene.file_Group = bpy.props.EnumProperty(
        name = "Export",
        items = [("SINGLEOBJ", "Individual Assets", "", 1),
                ("GROUPOBJ", "Group Assets", "", 2),
                ("SCENEOBJ", "Scene Export", "", 3)],
        description="export individual assets, one file with all the assets grouped or the scene")
    bpy.types.Scene.file_extention = bpy.props.EnumProperty(
        name = "File Extention",
        items = [("FBX", "FBX", "", 1),
                ("OBJ", "OBJ", "", 2)],
        description="type of file you will export")
    bpy.types.Scene.file_engine = bpy.props.EnumProperty(
        name = "Engine",
        items = [("UNITY", "Unity", "", 1),
                ("UE4", "UE4", "", 2),
                ("UDK", "UDK", "", 3)],
        description="the engine that you are exporting to")
    
    #plugin Display
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        #strings
        row = layout.row()
        row.prop(scene, "file_dir")
        row = layout.row()
        row.prop(scene, "file_name")
        
        #enums
        row = layout.row()
        row.prop(scene, "file_extention", expand=True)
        row = layout.row()
        row.prop(scene, "file_engine", expand=False)
        row.prop(scene, "file_Group", expand=False)

        #export Button
        row = layout.row()
        row.scale_y = 4.0
        row.operator("export.game_export")

#loops through and changes location
def ObjectLocation(thisBool, ass ,loc):
    x=0    
    for obj in ass:
        obj.select = True

        if(thisBool == True):
            obj.location = Vector((0,0,0))
        else:
            obj.location = loc[x]

        obj.select = False
        x += 1
    x=0
    return {'FINISHED'}        

def SceneExport(size, up, forw):
    scene = bpy.context.scene

    obj_active = scene.objects.active
    bpy.ops.object.select_all(action='DESELECT')
    scene.objects.active = obj_active

    if not os.path.exists(scene.file_dir):
        os.makedirs(scene.file_dir)

    if scene.file_extention == "FBX":
         fn = scene.file_dir + scene.file_name + ".fbx"
         bpy.ops.export_scene.fbx(
             filepath=fn,
             global_scale=size,
            axis_up=up,
            axis_forward=forw)
    else:
        fn = scene.file_dir + scene.file_name + ".obj"
        bpy.ops.export_scene.obj(
            filepath=fn,
            global_scale=size,
            axis_up=up,
            axis_forward=forw,
            group_by_object=False,
            use_blen_objects=True)
    return {'FINISHED'}
     
def SingleExport(size, up, forw):
    scene = bpy.context.scene

    obj_active = scene.objects.active
    bpy.ops.object.select_all(action='DESELECT')

    if not os.path.exists(scene.file_dir):
        os.makedirs(scene.file_dir)

    if scene.file_extention == "FBX":
        for obj in bpy.data.objects:

            obj.select = True
            scene.objects.active = obj

            fn = scene.file_dir + obj.name + ".fbx"
            bpy.ops.export_scene.fbx(
                use_selection=True,
                filepath=fn,
                global_scale=size,
                axis_up=up,
                axis_forward=forw)

            obj.select = False
    else:
        for obj in bpy.data.objects:

            obj.select = True
            scene.objects.active = obj

            fn = scene.file_dir + obj.name + ".obj"
            bpy.ops.export_scene.obj(
                use_selection=True,
                filepath=fn,
                global_scale=size,
                axis_up=up,
                axis_forward=forw,
                group_by_object=False,
                use_blen_objects=True)
            obj.select = False
    scene.objects.active = obj_active
    return {'FINISHED'}

def GroupExport(size, up, forw):
    scene = bpy.context.scene

    if scene.file_extention == "FBX":
        SceneExport(size, up, forw)
    else:
        obj_active = scene.objects.active
        bpy.ops.object.select_all(action='DESELECT')
        scene.objects.active = obj_active

        if not os.path.exists(scene.file_dir):
            os.makedirs(scene.file_dir)

        fn = scene.file_dir + scene.file_name + ".obj"
        bpy.ops.export_scene.obj(
            filepath=fn,
            global_scale=size,
            axis_up=up,
            axis_forward=forw,
            group_by_object=True,
            use_blen_objects=False)
    return {'FINISHED'}

#Export Script
class OBJECT_OT_GameExportButton(bpy.types.Operator):
    bl_idname = "export.game_export"
    bl_label = "Engine Export" 
    
    def execute(self, context):
        #vars
        scene = bpy.context.scene
        selection = bpy.context.selected_objects
        locations = []
        assets = bpy.data.objects

        #got assets locations
        for obj in assets:
            obj.select = True
            locations.append(Vector(obj.location))
            obj.select = False

        #engine Types
        if scene.file_engine == "UNITY":
            print("UNITY")
            expSize = 1
            expUp = 'Y'
            expForw = '-Z'
        elif scene.file_engine == "UE4":
            print("UE4")
            expSize = 100
            expUp = 'Z'
            expForw = '-Y'
        elif scene.file_engine == "UDK":
            print("UDK")
            expSize = 64
            expUp = 'Z'
            expForw = '-Y'
        
        #export
        if scene.file_Group == "SCENEOBJ":
            SceneExport(expSize, expUp, expForw)

        elif scene.file_Group == "GROUPOBJ":
            ObjectLocation(True, assets, locations)
            GroupExport(expSize, expUp, expForw)
            print("nope")

        elif scene.file_Group == "SINGLEOBJ":
            ObjectLocation(True, assets, locations)
            SingleExport(expSize, expUp, expForw)
            print("nope")
        
        #reset view
        ObjectLocation(False, assets, locations)

        for obj in selection:
            obj.select = True

        return {'FINISHED'}

#register   
def register():
    bpy.utils.register_class(GameExport)
    bpy.utils.register_class(OBJECT_OT_GameExportButton)

def unregister():
    bpy.utils.unregister_class(GameExport)
    bpy.utils.register_class(OBJECT_OT_GameExportButton)

if __name__ == "__main__":
    register()
