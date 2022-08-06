import shutil

import fiona
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, Polygon
import pathlib as pt
import os

folder_path = pt.Path(r'D:\TempData\CroppedData')
destination = pt.Path(r'D:\TempData')
data = []
csv_headers = ['filename', 'location', 'sensor_id', 'frame_number', 'latitude', 'longitude']
folder_list = os.listdir(folder_path)

for i,folder in enumerate(folder_list):
    image_list = os.listdir(folder_path / folder)
    for j,  image in enumerate(image_list):
        image_name = image.replace('.png', '').split('_')
        temp_data = dict.fromkeys(csv_headers)
        temp_data['filename'] = image
        temp_data['location'] = folder_path / folder / image
        temp_data['sensor_id'] = image_name[2]
        temp_data['frame_number'] = image_name[4]
        temp_data['latitude'] = format(float(image_name[8]), '.10f')
        temp_data['longitude'] = format(float(image_name[9]), '.10f')
        data.append(temp_data)

data_df = pd.DataFrame(data)
data_df.to_csv(destination / 'CroppedValidationData_08-05.csv')
