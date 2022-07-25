import glob
import re
import pathlib
import os
import subprocess
import sys
from multiprocessing import Pool
import multiprocessing
import time
import csv
import pathlib as path
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

debug = False

try:
    time.clock()
except:
    time.process_time()

# tree = ET.parse(r"T:\current\Users\Staff\Jiztom\Python_Projects\Image_Extraction_Template\Multi-OS\parameters.xml")
# root = tree.getroot()
# elements = root.findall('*')
#
# fileLoc_str = elements[1].text
# fileloc = pathlib.Path(elements[1].text)
# extrLoc = pathlib.Path(elements[2].text)
# imextXML = pathlib.Path(elements[3].text)
# # name_format = elements[4].text
# Console = elements[4].text
# process = 1
# CSV_check = 0

fileLoc_str = sys.argv[1]
fileloc = pathlib.Path(sys.argv[1])
extrLoc = pathlib.Path(sys.argv[2])
imextXML = pathlib.Path(sys.argv[3])
# name_format = sys.argv[4]
Console = sys.argv[4]
process = int(sys.argv[5])
CSV_check = int(sys.argv[6])
# print(Console)

with open(extrLoc, 'r') as f:
    if debug:
        print("Reading the data list")
    reader = csv.reader(f)
    data = list(reader)
    # CAN_Log = path.Path(data[1][0])
    if debug:
        print("Successfully read data list.")

with open(imextXML, 'r') as file:
    if debug:
        print("Reading the master XML File")
    filedata = file.read()
    if debug:
        print("Successful reading the Master XML file to memory.")


def parprocfun(file):

    destLoc = path.Path(data[0][1])

    if CSV_check:
        csv_data    = file.split(',')
        temp_file   = csv_data[5] + '\\' + csv_data[6] + '.log'
        log_name = csv_data[6]
        file_path   = path.Path(temp_file)
        start_time  = csv_data[8]
        stop_time   = csv_data[9]
        logger_name = csv_data[12]
    else:
        file_path = path.Path(file)

    # This creates the a new directory reference and this will be called.
    newdir = destLoc / file_path.parent.name / file_path.stem
    if debug:
        print(f"The new directory generated = {str(newdir)}")

    if not os.path.exists(newdir):
        print(f"{datetime.now().strftime('%m/%d/%Y %H:%M:%S')} : Running for file {file}")
        # Creating a unique folder for each log. This also prevents any issues with folder duplicates.
        if CSV_check:
            pathlib.Path(newdir).mkdir(parents=True, exist_ok=True)
            if debug:
                print(f"Folder {newdir} Created successfully")
        else:
            # folder_temp = destLoc / file_path.parent.name
            pathlib.Path(newdir).mkdir(parents=True, exist_ok=True)
            if debug:
                print(f"Folder {newdir} Created successfully")

        # Creating a pattern for log path
        relogpath = re.compile("(?<=<logName>).*(?=</logName>)", re.ASCII)
        filedatatemp = relogpath.sub(str(file_path).replace('\\', '/'), filedata)

        # Creating a pattern match for directory path and then replacing them in the XML file.
        if not CSV_check:
            redirpath = re.compile("(?<=<directoryPath>).*(?=</directoryPath>)", re.ASCII)
            cleaned = str(newdir).replace('\\', '/')
            # filedatatemp = redirpath.sub(str(newdir).replace('\\', '/'), filedatatemp)
            filedatatemp = redirpath.sub(cleaned, filedatatemp)
            # print(f'Cleaned newdir = {cleaned}')

        if len(data) != 1:
            for row in data[1:]:
                try:
                    temp = re.compile(f"(?<=<{str(row[0])}>).*(?=</{str(row[0])}>)", re.ASCII)

                    # Special case 1
                    if row[0] == 'logNameBase': # Condition for CAN asc file name extracted.
                        filedatatemp = temp.sub(str(file_path.stem).replace('\\', '/'), filedatatemp)
                        # print(f'{row[0]} works with {str(file_path.stem)} ')

                    # Special case 2
                    elif row[0] == 'defaultDirectoryPath': # location of the CAN log to be extracted.
                        can_dir = path.Path(row[1]) / file_path.parent.name

                        if not os.path.exists(can_dir): # Creating can folder incase it doesnt exist.
                            pathlib.Path(can_dir).mkdir(parents=True, exist_ok=True)
                            # print('Directory created successfully.')
                        # print(f'{row[0]} works with {str(can_dir)}')
                        filedatatemp = temp.sub(str(can_dir).replace('\\', '/'), filedatatemp)

                    # Incase directory path with different
                    elif row[0] == 'directoryPath':
                        filedatatemp = temp.sub(str(newdir).replace('\\', '/'), filedatatemp)

                    # Setting manual Log file for the Log
                    elif row[0] == 'manualLogPath':
                        mandir = destLoc / file_path.parent.name / str(logger_name + '.log')
                        filedatatemp = temp.sub(str(mandir).replace('\\', '/'), filedatatemp)

                    elif row[0] == 'startTs':
                        filedatatemp = temp.sub(str(start_time).replace('\\', '/'), filedatatemp)

                    elif row[0] == 'stopTs':
                        filedatatemp = temp.sub(str(stop_time).replace('\\', '/'), filedatatemp)

                    # All other elements
                    else:
                        filedatatemp = temp.sub(row[1].replace('\\', '/'), filedatatemp)
                except:
                    print(f"The file error = {sys.exc_info()[0]}")
        else:
            # print("No additional variables found.")
            pass
        try:
            temp_time = time.clock()
        except:
            temp_time = time.process_time()

        # Creating a temporary XML file with CPU runtime to prevent overwrite
        imextXML_temp = imextXML.stem + '_' + str((int(temp_time * 100000))) + '.xml'

        # Creating the cleaned version of the temp_path
        temp_path = path.Path(imextXML_temp)
        temp_path = temp_path.absolute()
        temp_path_str = str(temp_path).replace('\\', '/')
        # print(f"imexXML_temp = {imextXML_temp}")
        # print(f"absolute path = {temp_path}")
        # print(f"Cleaned proper format = {temp_path_str}")

        # Creating the local copy of the modified XML
        with open(imextXML_temp, 'w') as file:
            file.write(filedatatemp)

        # # do something with the updated line
        with open(os.devnull, 'w') as FNULL:
            # print([Console, str(temp_path_str)])
            subprocess.call([Console, str(temp_path_str)], stdout=FNULL, stderr=FNULL, shell=False)

        # Removing the temporarily created XML file.
        os.remove(imextXML_temp)
    else:
        pass
        print(f'The folder for {file} already exists.')


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()
    # starting time
    start = time.time()
    # print("The program has started")
    print(f"The number of multi process enabled : {process} ")
    print(fileloc)
    if CSV_check == 1:
        print("Processing from CSV")
        files = []
        s = ","
        with open(fileloc, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        data.pop(0)
        for line in data:
            files.append(s.join(line))
    else:
        files = glob.glob(fileLoc_str + r'\**\*.log', recursive=True)
    # print(files)
    with Pool(int(process)) as p:
        time.sleep(0.25)
        p.map(parprocfun, files)

    # end time
    end = time.time()

    # total time taken
    print(f"Runtime of the program is {convert(end - start)}")
