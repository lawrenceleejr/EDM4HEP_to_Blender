import bpy
import csv
import math

print("starting")

# basepath = "/Users/leejr/work/EDM4HEP_to_Blender/InputsFromFede_241101/muonGun_pT_50_250_reco.edm4hep.root"
# basepath = "/Users/leejr/work/EDM4HEP_to_Blender/InputsFromFede_241101/neutronGun_E_50_250_reco.edm4hep.root"
# basepath = "/Users/leejr/work/EDM4HEP_to_Blender/InputsFromFede_241101/photonGun_E_50_250_reco.edm4hep.root"
basepath = "/Users/leejr/work/EDM4HEP_to_Blender/InputsFromFede_241101/nuGun_digi_v0A.edm4hep.root"

# List of (file_path, scaling_factor) for each CSV file
csv_files = [
    (basepath+"_trackerHits.csv", 1.5),
    (basepath+"_caloHits.csv", 5),
    (basepath+"_muonHits.csv", 5),
]

# Delete all existing mesh objects (optional, if you want a clean scene)
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create an empty mesh and object to hold all cubes as a single object
master_mesh = bpy.data.meshes.new("CombinedMesh")
master_object = bpy.data.objects.new("CombinedObject", master_mesh)
bpy.context.collection.objects.link(master_object)

# Set the master object as active
bpy.context.view_layer.objects.active = master_object
master_object.select_set(True)

# Loop through each CSV file and its scaling factor
for csv_file_path, relative_scale in csv_files:
    print(csv_file_path)
    # Open the CSV file and read each line
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if present
        for irow,row in enumerate(reader):
            if irow%100==0:
                print(irow)
            # Read x, y, z, and scale values from each row by index
            x = float(row[0])  # Assuming x is in the first column (index 0)
            z = float(row[1])  # Assuming y is in the second column (index 1)
            y = float(row[2])  # Assuming z is in the third column (index 2)
            scale = math.log10(float(row[3])) * relative_scale  # Assuming scale is in the fourth column (index 3)
            
            # Create a temporary cube
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
            temp_cube = bpy.context.object  # Get the newly created cube
            
            # Scale the cube
            temp_cube.scale = (scale, scale, scale)
            
            # Apply transformations to make sure scaling is baked into the vertices
            bpy.context.view_layer.objects.active = temp_cube
            bpy.ops.object.transform_apply(scale=True)
            
            # Join the cube's mesh into the master object
            bpy.ops.object.select_all(action='DESELECT')
            temp_cube.select_set(True)
            master_object.select_set(True)
            bpy.context.view_layer.objects.active = master_object
            bpy.ops.object.join()  # Join the temporary cube into the master object

print("Finished creating a single mesh object from multiple CSV files with relative scaling.")

# Specify the path where you want to save the file
save_path = basepath+"_mesh.blend"

# Save the current Blender file
bpy.ops.wm.save_as_mainfile(filepath=save_path)