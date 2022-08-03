import os
import cv2
import pathlib as pt
import pandas as pd
import numpy as np
from PIL import Image
from tqdm import tqdm
from time import sleep
import shutil


def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale


source_folder = pt.Path(r'F:\CroppedData')
destination = pt.Path(r'F:\Machine_Sorted')

csv_headers = ['filename', 'location', 'bright/dark', 'brightness', ' moved']
count = 0
display_results = False

folder_list = os.listdir(source_folder)
data = []

pbar_main = tqdm(folder_list)
for folder in pbar_main:

    pbar_main.set_description("Processing %s" % folder)
    # print(f'Running for {folder}', end='\r')
    image_list = os.listdir(source_folder / folder)

    pbar_image = tqdm(image_list, leave=True)
    for img in pbar_image:
        # pbar_image.set_description("")
        temp_data = dict.fromkeys(csv_headers)
        image = Image.open(source_folder / folder / img)
        brightness = calculate_brightness(image)

        if brightness > 0.25:
            if display_results:
                print(f"{img}:{brightness}. Moving to target")
            temp_data['dark/bright'] = 'bright'
            count += 1
            pt.Path(destination / folder).mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_folder / folder / img, destination / folder / img)
            temp_data['moved'] = True
        else:
            if display_results:
                print(f"Dark Image : {brightness}")
            temp_data['dark/bright'] = 'dark'
            temp_data['moved'] = False

        temp_data['filename'] = img
        temp_data['location'] = source_folder / folder / img
        temp_data['brightness'] = brightness
        data.append(temp_data)

print(f"No of moved Imaged : {count}")
data_df = pd.DataFrame(data)
