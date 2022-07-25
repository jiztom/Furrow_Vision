##!/usr/bin/env python # Not sure if this is necessary in this case
# =============================================================================
"""
    File name: interpolationGPS.py
    Author: Felipe Varela Carvalho
    Date created: 5/24/2021
    Date last modified: 6/25/2021
    Python Version: 3.9
    Description: Script to interpolate data from file
"""
# =============================================================================
# Imports
import os
import pathlib as pt
import numpy as np
import shutil
import csv
from CANprocessing import get_list_of_files

# =============================================================================

# Hardcoded location of the starting script
'''This allows you to have this location and file handling for all types of OS'''
# Base_directory = pt.Path(r'T:\current\Projects\Deere\CPSI\2021\Digital Acre\Data Wrangling')
Base_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\MissingLog')

# Base_image_directory = pt.Path(r'T:\current\Projects\Deere\CPSI\2021\Digital Acre\Data Wrangling\Images')
Base_image_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\MissingLog\Images2')

# processed_CANfile_directory = pt.Path(r'T:\current\Projects\Deere\CPSI\2021\Digital Acre\Data Wrangling\CANfiles_processed')

processed_CANfile_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\MissingLog\CANfiles_processed')

# new_images_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\TestFolder\Images2')
new_images_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\MissingLog\ImagesProcessed')

# Directory for test
Base_directory_test = pt.Path(r'T:\ftp\seeding\FurrowVision\MACHINE_DATA\TEMPORARY\DigitalAcre\CANSNIFF')


# Returns latitude and longitude from CAN data row in format (example)
# 0.000000 1620152387.412609 0  14FF641Cx       Rx   d 8 66 FE 0C 9E 29 9B FE 02
def absolute_coordinate(data):
    lat_hex = data[10] + data[9] + data[8] + data[7]
    lat = int(lat_hex, 16) * 10 ** (-7) - 210
    long_hex = data[14] + data[13] + data[12] + data[11]
    long = int(long_hex, 16) * 10 ** (-7) - 210

    return lat, long


# Returns list of immediate sub-folders given root folder
def get_immediate_subfolders(folder):
    list_of_folders = [x[0] for x in os.walk(folder)]
    list_of_folders.pop(0)
    return list_of_folders


# Create new sub-folder in existing root folder
def create_subfolder(root, new_name):
    # check if folder exists
    new_directory = (os.path.join(root, new_name))
    if os.path.exists(new_directory):
        print("Folder already exists: " + new_directory)
        return 0
    else:
        # print(new_directory)
        os.mkdir(new_directory)
    return new_directory


# Returns Longitude and Latitude interpolation from two rows from CAN data with a given image timestamp
# Can data format (example)
# 0.000000 1620152387.412609 0  14FF641Cx       Rx   d 8 66 FE 0C 9E 29 9B FE 02
def find_long_and_lat(data1, data2, timefromimage):
    # Handles case where only one timestamp was found
    if data2 == 0:
        return absolute_coordinate(data1)

    # Find the latitude and longitude from hex values
    lat1, long1 = absolute_coordinate(data1)
    lat2, long2 = absolute_coordinate(data2)

    # Polynomial fit
    latitudes = [lat1, lat2]
    time_stamps = [float(data1[1]), float(data2[1])]
    coefficients = np.polyfit(time_stamps, latitudes, 1)
    lat_equation = np.poly1d(coefficients)

    longitudes = [long1, long2]
    coefficients = np.polyfit(time_stamps, longitudes, 1)
    long_equation = np.poly1d(coefficients)

    # Find image coordinate
    image_lat = lat_equation(float(timefromimage))
    image_long = long_equation(float(timefromimage))

    # print("Latitude and longitude 1: ", lat1, long1)
    # print("Latitude and longitude 2: ", lat2, long2)

    return image_lat, image_long


# Main
if __name__ == '__main__':
    print('------------Start of Program:------------\n')
    # Get all sub-folder paths
    images_folder_list = get_immediate_subfolders(Base_image_directory)
    # Sort sub-folders
    images_folder_list.sort(key=lambda x: x.split('AmesISU_')[1])
    # print(images_folder_list)
    info_list = []
    for counter in range(len(images_folder_list)):
        # Get all image names
        current_directory = images_folder_list[counter]
        image_paths = list(pt.Path(current_directory).rglob('*.png'))  # List with all image absolute paths
        image_paths.sort()  # Sort the paths to match file explorer

        # Open list of files with CAN data and unix time
        CANfiles = get_list_of_files(processed_CANfile_directory)
        CANfiles.sort()
        log_name = CANfiles[counter]
        lines = []  # List with all of the information from CAN file
        log_number = log_name[:log_name.find("_perception")]
        with open(log_name, 'r') as my_file:  # This should open the CAN file with the relative timestamps
            for line in my_file:
                if line[2].isdigit():  # Makes sure that we are only reading data (ignoring headers)
                    lines.append(line.split())  # Add to the list with row data

        # Create new folder where images are going to be saved in
        new_image_path = create_subfolder(new_images_directory, os.path.basename(current_directory))
        if new_image_path == 0:
            continue
        # Loop over all images and find all GPS interpolation locations

        for i in range(len(image_paths)):
            image_path = str(image_paths[i])
            # Get Unix time from image label
            image_name = os.path.basename(image_path)  # Extract image name as string
            image_time = image_path[-19: len(image_path) - 4]  # Extract image Unix time (-4 removes .png)
            camera_number = image_name.split("image_sensorid_", 1)[1]
            camera_number = camera_number[0]
            # print("image_name: ", image_name)
            # print("image_time: ", image_time)
            # print("camera_number: ", camera_number)

            # Algorithm to find closest pair of numbers from timestamp
            current_num = 0.0
            last_visited = 0
            latitude = 0
            longitude = 0
            for j in range(len(lines)):
                if lines[j][3] == "0CFEF39Cx":
                    current_num = lines[j][1]
                    if current_num >= image_time:
                        if last_visited == 0:
                            latitude, longitude = find_long_and_lat(lines[j][:], 0,
                                                                    image_time)  # Handles case if image coincides with
                            # first timestamp
                        else:
                            latitude, longitude = find_long_and_lat(lines[last_visited][:], lines[j][:], image_time)
                        break
                    last_visited = j
                else:
                    continue

            # Generate camera offset given camera number and table:
            # ===========================================================================================
            #                            /   Row 1       /   Row 2        /   Row 3        /   Row 4
            # Offset Longitude factor    /  -0.0000138   /   -0.0000046   /   0.0000046    /   0.0000138
            # ===========================================================================================
            camera1_offset = -0.0000138
            camera2_offset = -0.0000046
            camera3_offset = 0.0000046
            camera4_offset = 0.0000138

            if camera_number == '1':
                longitude = longitude + camera1_offset
            elif camera_number == '2':
                longitude = longitude + camera2_offset
            elif camera_number == '3':
                longitude = longitude + camera3_offset
            elif camera_number == '4':
                longitude = longitude + camera4_offset
            # print("image latitude and longitude: ", latitude, longitude)

            # Copy image over and rename it with new latitude and longitude
            # new_image_path = pt.Path(r'C:\Users\abe_felipec\PycharmProjects\timestapCANFiles\exportedImages')
            shutil.copy2(image_path, new_image_path)
            old_name = os.path.join(new_image_path, image_name)
            image_new_name = image_name[0:-4] + '_GPS_' + format(latitude, '.10f') + '_' + format(longitude,
                                                                                                  '.10f') + '.png'
            # print(image_new_name)
            new_name = os.path.join(new_image_path, image_new_name)
            os.rename(old_name, new_name)
            # print("Image new name", new_name)
            # print("\n")

            # Add to image information and its attributes to list that is going to be later added to a csv file
            info = [os.path.basename(log_name), image_new_name, image_time, camera_number, format(latitude, '.10f'), format(longitude, '.10f')]
            info_list.append(info)

    print("------------End of Program:------------ \n")
