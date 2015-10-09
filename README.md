# Blender-to-Game-Engine-Addon

#Requirements
This was developed for blender **2.74**, I haven’t tested it in earlier versions so it may cause issues.

#Overview
This addon is used to export your scene from Blender to your game engine of choice. 

#Features
- Load model(s) to file directory and change names
- Export the scene objects as **.obj** or **.fbx** in one group or individually
- Adjust size and axis of objects depending on the engine (current engine Unity, UDK, UE4)
- Your selections, directory and names are saved to the scene so they will remain if you quit

#Installation
With Blender open and file downloaded, go to **File** > **User Preferences** > **Add-ons** > **Install from File**. 

Select *BlenderToGameEngine_Export.py* and in the addon list, search for *Blender to Game Engine Export* and select the checkbox and **Save User Settings**.

#How to Use
The export panel is in **Properties** > **Scene** and it is called Game Engine Export.

With every object in the scene, make sure that;
- it is correctly named
- the pivot point is correctly positioned 

##File Directory
This is where you name the directory of where the file will be saved. It will create the path if it doesn’t exist.

Place it in the back end files for your project and the engine will refresh the asset files (tested in Unity).

##File Name
This is the output file name for grouped and scene export.

##Engine
Select the engine you are exporting to. 

Currently suppory unity, UDK and UE4 setup. If you have a different engine, please name it and state the scale of BU, up and forward axis in the comments.

##Export
there are 3 options are **Individual Assets**, **Group Assets** and **Scene Export**
- Individual Assets will move all the objects to the center of the scene and export each one with the object name
- Group Assets moves all the objects to the center of the scene and saves out the scene with all the individual elements
- Scene Export will save out the scene keeping the location of objects. OBJ will get grouped to one mesh

As you adjust the settings, they will be saved to the scene. They will be saved when you quit.

When you make an edit and are ready to export. Click Engine Export and it will save all objects to the directory.

