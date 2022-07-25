import math
import os
import shutil
import random
import pathlib as pt

NUMBER_OF_OUTPUT_FOLDERS = 7
# FILE_INPUT = pt.Path(r'T:\current\Projects\Deere\CPSI\2021\Digital Acre\Data Wrangling\Images_Processed_TreatmentZones')
FILE_INPUT = pt.Path(r'C:\Users\abe_felipec\Desktop\TestFolder\Images3')
# FILE_OUTPUT = pt.Path(r'T:\current\Projects\Deere\CPSI\2021\Digital Acre\Data Wrangling\Images_Bulk_Labeling')
FILE_OUTPUT = pt.Path(r'C:\Users\abe_felipec\Desktop\TestFolder\Images4')


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


def get_immediate_subfolders(folder):
    list_of_folders = [x[0] for x in os.walk(folder)]
    list_of_folders.pop(0)
    return list_of_folders


def get_random_files(file_list, N):
    return random.sample(file_list, N)


def copy_files(random_files, input_dir, output_dir):
    for file in random_files:
        shutil.move(os.path.join(input_dir, file), output_dir)


def main(input_dir, output_dir, N):
    file_list = get_list_of_files(input_dir)
    random_files = get_random_files(file_list, N)
    copy_files(random_files, input_dir, output_dir)


# Program
print("Fetching Files")
in_file_list = get_list_of_files(FILE_INPUT)
out_folder_list = get_immediate_subfolders(FILE_OUTPUT)
print("Found " , len(in_file_list) , "files")
print("Found " , len(out_folder_list) , " output files")
N = math.floor(len(in_file_list) / NUMBER_OF_OUTPUT_FOLDERS)
remainder = len(in_file_list) % NUMBER_OF_OUTPUT_FOLDERS

for i in range(len(out_folder_list)):
    N = math.floor(len(in_file_list) / NUMBER_OF_OUTPUT_FOLDERS)
    if i == 0:
        N = N + remainder
    main(FILE_INPUT, out_folder_list[i], N)

