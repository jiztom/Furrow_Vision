# Imports
import os
import pathlib as pt
import numpy as np
import shutil
import csv
from CANprocessing import get_list_of_files

# Base_image_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\TestFolder\Images2')

Base_image_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\MissingLog\ImagesProcessed')


# Returns list of immediate sub-folders given root folder
def get_immediate_subfolders(folder):
    list_of_folders = [x[0] for x in os.walk(folder)]
    list_of_folders.pop(0)
    return list_of_folders


def get_list_of_files(dir_name):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dir_name)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


subfolders = get_immediate_subfolders(Base_image_directory)
info_list = []
for counter in range(len(subfolders)):
    log_name = os.path.basename(subfolders[counter])
    list_of_files = get_list_of_files(subfolders[counter])
    for i in range(len(list_of_files)):
        image_name = list_of_files[i]
        image_time = os.path.basename(image_name).split('_')[6]
        camera_number = os.path.basename(image_name).split('_')[2]
        latitude = str(os.path.basename(image_name))[-32: -19]
        longitude = str(os.path.basename(image_name))[-18: -4]
        if latitude[0] == 'S' or latitude[0] == 'P':
            latitude = "0.000000000"
            longitude = "0.000000000"
        print(log_name, image_name, image_time, camera_number, latitude, longitude)
        info = [log_name, os.path.basename(image_name), image_time, camera_number, latitude, longitude]
        info_list.append(info)

with open("ImageData_DigitalAcre_trials.csv", 'w', newline='') as file:
# with open("ImageData_DigitalAcre.csv", 'w', newline='') as file:
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    # Write header
    wr.writerow(['Log Name', 'Image Name', 'Image Time Stamp', 'Camera Number', 'Latitude', 'Longitude'])
    # Write data
    wr.writerows(info_list)
 # Done
