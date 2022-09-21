import os
import sys
from PIL import Image
import pathlib as pt
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


if __name__ == '__main__':
    # file = r'D:\Furrow Vision\PythonProject_Furrow\ImageSeperator\SampleImage' \
    #                  r'\image_sensorid_1_frame_28786_ts_1652737111.3495_GPS_42.0441175000_-93.7735324000.png '
    destination = pt.Path(r'E:\Furrow\Label_data')
    side_destination = pt.Path(r'E:\Furrow\dark')
    source = pt.Path(r'D:\TempData\LabelData')
    count = 0
    darkcount = 0
    for num, file in enumerate(os.listdir(source)):

        image = Image.open(source / file)
        brightness = calculate_brightness(image)
        image_rotate = image

        if brightness > 0.30:
            shutil.copy2(source / file, destination / file)
            count += 1
        else:
            darkcount += 1
            shutil.copy2(source / file, side_destination / file)
        print(f"{num} - Image : {brightness}| Bright images: {count} ; Dark Images: {darkcount}", end='\r')
    print(f"No of moved Imaged : {count}")