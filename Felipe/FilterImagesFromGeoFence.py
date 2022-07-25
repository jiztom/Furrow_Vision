import os.path

import pandas as pd
import pathlib as pt
import shutil
from CANprocessing import get_list_of_files
from interpolationGPS import get_immediate_subfolders

# Input: CSV file with image names

df = pd.read_csv(r'ImageData_DigitalAcre_Treatments.csv', index_col=0)

# Create list with all of image names
log_names = df['Log Name']
image_names = df['Image Name']

# Get unique logs in data set, aka the logs that we are actually using
logs = df['Log Name'].unique()
logs.sort()
print(logs)
# Create list with datasets for each unique log
data =[]
for i in range(len(logs)):
    data.append(df.loc[df['Log Name'] == logs[i]])

# Now data is a list where each item is a data frame of each used log

# Get list of image folders
image_files_locations = pt.Path(r'C:\Users\abe_felipec\Desktop\TestFolder\Images2')
new_image_files_locations = pt.Path(r'C:\Users\abe_felipec\Desktop\TestFolder\Images3')

# Create new directories for new images
for items in logs:
    path = os.path.join(new_image_files_locations,items)
    try:
        os.mkdir(path)
    except:
        print("Folder with the name already exists: " +items)

# Get old folder list and new folder list
folder_list = get_immediate_subfolders(image_files_locations)
new_folder_list = get_immediate_subfolders(new_image_files_locations)

counter = 0
test_counter = 0
for i in range(len(folder_list)):
    if os.path.basename(folder_list[i]) == logs[counter]:
        file_list = get_list_of_files(folder_list[i])
        for j in range(len(file_list)):
            if os.path.basename(file_list[j]) in data[counter]['Image Name'].to_numpy():
                shutil.copy2(file_list[j], new_folder_list[counter])
        counter = counter + 1
    else:
        continue

print(test_counter)