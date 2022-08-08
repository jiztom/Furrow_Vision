import pathlib as pt
import shutil
import os
import pandas as pd

source_directory = pt.Path(r'D:\TempData\CroppedData')
destination_directory = pt.Path(r'D:\TempData\LabelData')

folder_list = os.listdir(source_directory)

csv_header = ['filename', 'location', 'source_folder']
data = []
for folder in folder_list:
    image_list = os.listdir(source_directory / folder)
    for image in image_list:
        shutil.copy2(source_directory / folder / image, destination_directory / image)
        temp_data = dict.fromkeys(csv_header)
        temp_data['filename'] = image
        temp_data['location'] = destination_directory / image
        temp_data['source_folder'] = folder
        data.append(temp_data)

data_df = pd.DataFrame(data)
data_df.to_csv(destination_directory / 'LabelReadyData.csv')

