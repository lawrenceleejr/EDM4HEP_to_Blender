import bpy

from datetime import datetime

# Get the current timestamp as a filename-safe string
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

physicsObjects = ["Muon","Neutron","Photon","All"]

basepath = "/Users/leejr/work/MuonColliderBlender/"



def render_callback(scene):
    # Check if rendering is in progress
    if bpy.data.scenes[0].render.is_rendering:
        print("Rendering in progress...")
    else:
        print("Rendering complete.")
        return None  # Stop the timer

    return 1.0  # Check again in 1 second

# Register the callback to check render status every second
bpy.app.timers.register(render_callback)

print("starting loop")

for focusObject in physicsObjects:
    for showBIB in [0,1]:
        print("------",focusObject,showBIB)

        # Disable rendering for specified objects
        for obj_name in physicsObjects:
            print(obj_name)
            obj = bpy.data.objects.get(obj_name)
            if obj:
                obj.hide_render = True
                if obj_name==focusObject:
                    obj.hide_render = False
                if focusObject=="All":
                    obj.hide_render = False
            else:
                print(f"Object '{obj_name}' not found.")


        obj = bpy.data.objects.get("BIB")
        if showBIB:
            obj.hide_render = False
        else:
            obj.hide_render = True


        # Define the names of the cameras to enable in multi-view mode
        cameras_to_enable = [f"_{focusObject}1", f"_{focusObject}2"]

        if focusObject=="All":
            cameras_to_enable = ["_Photon2"]

        # Enable multi-view and set specific cameras
        bpy.context.scene.render.use_multiview = True


        for view in bpy.context.scene.render.views:
            view.use = False
            if view.name in cameras_to_enable:
                view.use = True

        # Set the render path and output settings
        output_path = f"{basepath}/{timestamp_str}_Render_{focusObject}_BIB{showBIB}.png"
        bpy.context.scene.render.filepath = output_path

        # Perform the render
        bpy.ops.render.render(animation=False, write_still=True)



### All with varied focal lengths with orthographic

focusDistances = [
    5500, #photon
    6300, #muon
    8100, #neutron
    12000, #blurry
    ]
# not using the lists in the end since I can't change the focus distance in a script (arggggg)


# Enable all physics objects
for obj_name in physicsObjects[:-1]:
    obj = bpy.data.objects.get(obj_name)
    if obj:
        obj.hide_render = False
    else:
        print(f"Object '{obj_name}' not found.")

cameras_to_enable = [
    "_OrthoDOF5500",
    "_OrthoDOF6300",
    "_OrthoDOF8100",
    "_OrthoDOF12000",    
    ]

# Enable multi-view and set specific cameras
bpy.context.scene.render.use_multiview = True

for view in bpy.context.scene.render.views:
    view.use = False
    if view.name in cameras_to_enable:
        view.use = True

# Set the render path and output settings
output_path = f"{basepath}/{timestamp_str}_Render_All_Ortho.png"
bpy.context.scene.render.filepath = output_path

# Perform the render
bpy.ops.render.render(animation=False, write_still=True)
