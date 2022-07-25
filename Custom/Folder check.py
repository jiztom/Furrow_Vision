import os
import pathlib as pt
import pandas as pd
import glob
import math


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


Base_image_directory = pt.Path(r'E:\2022_DigitalAcre_FurrowVisionData')

processed_CANfile_directory = pt.Path(r'E:\CanSniff\2022_DigitalAcre_FurrowVisionData')

new_images_directory = pt.Path(r'F:\GPSProcessed')

report_directory = pt.Path(r'F:\Reports')

source_directory = pt.Path(r'T:\current\Projects\Deere\CPSI\2022\Digital Acre\2022_DigitalAcre_FurrowVisionData')

folder_list = os.listdir(Base_image_directory)

empty_folder = []
for i, folder in enumerate(folder_list):
    if not os.listdir(Base_image_directory / folder):
        temp_file = source_directory / f'{folder}.log'
        file_size = temp_file.stat().st_size
        converted_size = convert_size(file_size)
        empty_folder.append([folder, file_size, converted_size])
        # print(f'Folder {folder} is empty')

print('Result:')
print(f'Folders containing data = {len(folder_list) - len(empty_folder)}')
print(f'Empty folders = {len(empty_folder)}')
empty_pd = pd.DataFrame(empty_folder)
print('---------------------------------------------')
print('Empty Folders')
if bool(empty_folder):
    print(empty_pd)

# Get all sub-folder paths in the image folder
image_folder_list = os.listdir(Base_image_directory)
asc_files = glob.glob(str(processed_CANfile_directory) + "**/*.asc", recursive=True)
cansniff_files = glob.glob(str(processed_CANfile_directory) + "**/*.cansniff", recursive=True)
source_files = glob.glob(str(source_directory) + "**/*.log", recursive=True)

data_dict = {}
empty_dict = []
for x in image_folder_list:
    # temp_dict = dict.fromkeys(['cansniff', 'asc'], 1)
    temp_dict = {}
    for y in cansniff_files:
        # print(x,y)
        if x in y:
            temp_dict['cansniff'] = y
            # temp_dict['count'] += 1
    for y in asc_files:
        # print(x,y)
        if x in y:
            temp_dict['asc'] = y
    data_dict[x] = temp_dict

for item in data_dict:
    temp_dict1 = data_dict[item]
    # print(data1['cansniff'])
    if not bool(temp_dict1):
        empty_dict.append(item)
        print(f"popped {item}")

size_list = []
for item in empty_dict:
    temp_file = source_directory / f'{item}.log'
    file_size = temp_file.stat().st_size
    converted_size = convert_size(file_size)
    size_list.append([item, file_size, converted_size])

temp_list = []
for x in image_folder_list:
    # temp_dict = dict.fromkeys(['cansniff', 'asc'], 1)
    # temp_dict = {}
    count = 0
    for y in cansniff_files:
        # print(x,y)
        if x in y:
            count += 1
    if count > 1:
        print(f'Counte greater than 1 :{x}')
    temp_list.append([x, count])
    # temp_dict['count'] += 1

missing_folder = []
print("_______________________________________________________________")
for x in cansniff_files:
    temp = x.split('\\')[-1][19:]
    found = True
    count = 0
    for y in image_folder_list:
        if y in x:
            found = False
            count += 1
    # print(temp, count)
    if found:
        print(temp)

data_pass = pd.DataFrame(size_list)
if bool(size_list):
    data_pass.to_csv(pt.Path(r'F:') / 'MissingData.csv', header=['filename', 'bytes', 'file size'])


empty_gps_folder = []
gps_image_list = os.listdir(new_images_directory)
for i, folder in enumerate(gps_image_list):
    if not os.listdir(new_images_directory  / folder):
        empty_gps_folder.append(folder)

print('THe empty GPS flder')
empty_gps_pd = pd.DataFrame(empty_gps_folder)
if bool(empty_gps_folder):
    print(empty_gps_pd)

incomplete_data = []
unprocessed = []
for folder in image_folder_list:
    image_number = os.listdir(Base_image_directory/folder)
    try:
        gps_image = os.listdir(new_images_directory/folder)
        print(len(image_number), len(gps_image))
        if len(image_number) != len(gps_image):
            incomplete_data.append(folder)
    except:
        print(f'Folder {folder} not processed yet')
        unprocessed.append(folder)
print("--------------------------")
print('GPS Statistics')
incomplete_pd = pd.DataFrame(incomplete_data)
unprocessed_pd = pd.DataFrame(unprocessed)
print('incomplete data')
if bool(incomplete_data):
    print(incomplete_pd)
else:
    print("No incomplete folders.")
print("unprocessed data")
if bool(unprocessed):
    print(unprocessed_pd)
else:
    print("no unprocessed data")
