##!/usr/bin/env python # Not sure if this is necessary in this case
# =============================================================================
"""
    File name: CANprocessing.py
    Author: Felipe Varela Carvalho
    Date created: 5/21/2021
    Date last modified: 6/24/2021
    Python Version: 3.9
    Description: Script to add timestamps to CAN data for Digital Acre project at Iowa State University
"""
# =============================================================================
# Imports
import os
import pathlib as pt
from DisplayablePath import DisplayablePath

# =============================================================================


# 1. Import file cansniff and original CAN file
# 2. Generate new CAN file to not overwrite original CAN file
# 3. Add timestamp offset from cansniff (Unix time on first line of cansniff) as new column on the CAN file
# 3.1. With that, add timestamp on can file to new Unix column
# 4. Save and close new file somewhere

# Hardcoded location of the starting script


'''This allows you to have this location and file handling for all types of OS'''
# Base_directory = pt.Path(r'T:\current\Projects\Deere\CPSI\2021\Digital Acre\Data Wrangling')
Base_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\MissingLog')

# new_CANfile_directory = pt.Path(r'T:\current\Projects\Deere\CPSI\2021\Digital Acre\Data Wrangling\CANfiles_processed')

new_CANfile_directory = pt.Path(r'C:\Users\abe_felipec\Desktop\MissingLog\CANfiles_processed')


# Create list of directories
# Enter first directory
# Find CANSNIFF file and save uix time
# Find CANFILE
# Crete new canfile with added UNIX timestamp column
# Save it on the approriate folder
# Move on to next folder

def get_list_of_files(dir_name):
    '''
    :param dir_name:
    :return:
    function: Get a list of the files of the type we are looking for in the folder

    '''
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


# Main
if __name__ == '__main__':
    print('------------Start of Program:------------\n')

    # open CANSNIFF (.asc) file and extract first time stamp (follows CANSNIFF formatting)
    CANSNIFF_file_directory = Base_directory / 'CANSNIFFfiles'
    # Generate a list of all of the files in the CANSNIFF directory with absolute paths
    CANSNIFF_list_files = get_list_of_files(CANSNIFF_file_directory)
    # Sort list given file data ignoring path and extraction date/time
    CANSNIFF_list_files.sort(key=lambda x: x.split('_AmesISU_')[1])

    # open CANFILE (.asc) file
    CAN_file_directory = Base_directory / 'CANfiles'
    # Generate a list of all of the files in the CAN directory with absolute paths
    CAN_list_files = get_list_of_files(CAN_file_directory)
    # Sort list given file data ignoring path and extraction date/time
    CAN_list_files.sort(key=lambda x: x.split('_AmesISU_')[1])

    # paths = DisplayablePath.make_tree(Base_directory)
    # Loop through every iteration of CANSNIFF files
    for counter in range(len(CANSNIFF_list_files)):
        # Extract the time offset value (Unix)
        time_offset = open(CANSNIFF_list_files[counter], 'r').readline().rstrip().split()[4]
        # Add time offset to dataframe
        output_file_name = new_CANfile_directory /CAN_list_files[counter].split('_AmesISU_')[1]
        outFile = open(output_file_name, "w")

        with open(CAN_list_files[counter], 'r') as my_file:  # Change file location
            for line in my_file:
                reference_time = line.split()[0]  # Extract reference time to be added to Unix time
                try:
                    reference_time = float(time_offset) + float(reference_time)
                    new_row = line[:10] + ' ' + format(reference_time, '.6f') + line[10:]
                except:
                    new_row = line
                outFile.write(new_row)
            print("File with the name of " + str(output_file_name) + " was created\n")
        outFile.close()

    print("------------End of Program:------------ \n")
