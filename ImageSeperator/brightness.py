import os
import sys
from PIL import Image
import pathlib as pt


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
    destination = pt.Path(r'D:\Furrow Vision\PythonProject_Furrow\ImageSeperator\SampleImage')
    count = 0
    for file in os.listdir(destination):

        image = Image.open(destination / file)
        brightness = calculate_brightness(image)

        if brightness > 0.25:
            print(f"{file}:{brightness}. Moving to target")
            count += 1
        else:
            print(f"Dark Image : {brightness}")
    print(f"No of moved Imaged : {count}")