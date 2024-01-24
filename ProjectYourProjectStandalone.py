# Colton Cramer
# NR426
# 12/10/2023
# The purpose of this code is to batch project raster and vector files from a specified input folder to a desired map projection using ArcGIS's arcpy library, handling errors, and providing a summary of the conversion process.
# Lines 11, 14, and 17 will need to be updated based on the user's actual file paths and desired projection. WGS 1984 Web Mercator was used for this demo.

import arcpy
import os

# Specify the new path to the folder containing your raster and vector files
input_folder = r"C:\Users\cocramer\Desktop\Test Data Folder"

# Specify the well-formatted string representing your desired map projection
output_projection = "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"

# Specify the new path to the folder where you want to save the projected files
output_folder = r"C:\Users\cocramer\Desktop\Reprojection Output"

def batch_project(input_folder, output_projection, output_folder):
    """Project raster and vector files within the input folder to the specified projection."""

    # Set the workspace environment
    arcpy.env.workspace = input_folder

    # Get a list of all raster and vector files in the input folder
    raster_list = arcpy.ListRasters()
    vector_list = arcpy.ListFeatureClasses()

    # Define the output coordinate system
    out_coor_system = arcpy.SpatialReference()
    out_coor_system.loadFromString(output_projection)

    # Create an output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Counter for successful conversions
    success_count = 0

    # List to store files with undefined coordinate systems
    undefined_coor_system_files = []

    # Loop through and project raster files
    for raster in raster_list:
        output_raster = os.path.join(output_folder, f"proj_{os.path.basename(raster)[:8]}")
        if arcpy.Exists(output_raster):
            print(f"Skipping {os.path.basename(raster)} - Output file already exists.")
        else:
            try:
                arcpy.management.ProjectRaster(raster, output_raster, out_coor_system)
                success_count += 1
                print(f"Converted {os.path.basename(raster)} to {os.path.basename(output_raster)}")
            except arcpy.ExecuteError:
                print(f"Failed to project raster {os.path.basename(raster)}: {arcpy.GetMessages()}")

    # Loop through and project vector files
    for vector in vector_list:
        output_vector = os.path.join(output_folder, f"projected_{os.path.basename(vector)}")
        if arcpy.Exists(output_vector):
            print(f"Skipping {os.path.basename(vector)} - Output file already exists.")
        else:
            try:
                # Check if the input vector has a defined coordinate system
                in_coor_system = arcpy.Describe(vector).spatialReference
                if in_coor_system is None:
                    print(f"Skipping {os.path.basename(vector)} - Input coordinate system is not defined.")
                    undefined_coor_system_files.append(os.path.basename(vector))
                else:
                    arcpy.management.Project(vector, output_vector, out_coor_system)
                    success_count += 1
                    print(f"Converted {os.path.basename(vector)} to {os.path.basename(output_vector)}")
            except arcpy.ExecuteError:
                print(f"Failed to project vector {os.path.basename(vector)}: {arcpy.GetMessages()}")

    # Print a summary of files with undefined coordinate systems
    if undefined_coor_system_files:
        print(f"The following files were skipped due to undefined coordinate systems:")
        for filename in undefined_coor_system_files:
            print(f"- {filename}")

    print(f"Conversion completed. {success_count} layers successfully converted.")

# Call the batch_project function with the updated input and output parameters
batch_project(input_folder, output_projection, output_folder)
