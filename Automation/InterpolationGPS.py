""" InterploationGPS.py

    Author          : Jiztom Kavalakkatt Francis
    Date Created    : 07/08/2022
    Last Modified   : 09/04/2022
    Python Version  : 3.10.5
    Description     : This script allows for interpolating the image with the GPS data.
"""

# Declaring imports
import os
import pathlib as pt
import numpy as np
import shutil
import pandas as pd
import glob
from datetime import date
from PIL import Image

today = date.today()
date_print = today.strftime("%b-%d-%Y")


def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale


# Returns latitude and longitude from CAN data row in format (example)
# 0.000000 1620152387.412609 0  14FF641Cx       Rx   d 8 66 FE 0C 9E 29 9B FE 02
def absolute_coordinate(data):
    lat_hex = data[9] + data[8] + data[7] + data[6]
    lat = int(lat_hex, 16) * 10 ** (-7) - 210
    long_hex = data[13] + data[12] + data[11] + data[10]
    long = int(long_hex, 16) * 10 ** (-7) - 210

    return lat, long


# Returns Longitude and Latitude interpolation from two rows from CAN data with a given image timestamp
# Can data format (example)
# 0.000000 1620152387.412609 0  14FF641Cx       Rx   d 8 66 FE 0C 9E 29 9B FE 02
def find_long_and_lat(data1, data2, imagetime, unix_timestamp):
    '''

    :param data1: previous data
    :param data2: current data
    :param timefromimage: time to predict.
    :return:
    '''
    poly_fit_value = 1
    timefromimage = imagetime #- unix_timestamp
    # Handles case where only one timestamp was found
    if data2[0] == 0:
        return absolute_coordinate(data1)

    # Find the latitude and longitude from hex values
    lat1, long1 = absolute_coordinate(data1)
    lat2, long2 = absolute_coordinate(data2)
    # print(f"lat1 : {lat1}, long1: {long1}")
    # print(f"lat2 : {lat2}, long1: {long2}")

    time_stamps = [float(data1[1]) + unix_timestamp, float(data2[1]) + unix_timestamp]

    # Polynomial fit
    latitudes = [lat1, lat2]

    coefficients = np.polyfit(time_stamps, latitudes, poly_fit_value)
    lat_equation = np.poly1d(coefficients)

    longitudes = [long1, long2]
    coefficients = np.polyfit(time_stamps, longitudes, poly_fit_value)
    long_equation = np.poly1d(coefficients)

    # Find image coordinate
    image_lat = lat_equation(float(timefromimage))
    image_long = long_equation(float(timefromimage))

    # print("Latitude and longitude 1: ", lat1, long1)
    # print("Latitude and longitude 2: ", lat2, long2)
    # print(image_lat, image_long)
    return image_lat, image_long


if __name__ == "__main__":

    debug = False
    GPS_offset = 4
    b_factor = 0.25
    print('------------Start of Program:------------\n')

    Base_image_directory = pt.Path(r'E:\2022_DigitalAcre_FurrowVisionData')

    processed_CANfile_directory = pt.Path(r'E:\CanSniff\2022_DigitalAcre_FurrowVisionData')

    new_images_directory = pt.Path(r'D:\TempData\GPSProcessed')

    report_directory = pt.Path(r'D:\TempData\Report')

    # Directory for test
    Base_directory_test = pt.Path(r'D:\TempData\Report')

    # Get all sub-folder paths in the image folder
    image_folder_list = os.listdir(Base_image_directory)
    asc_files = glob.glob(str(processed_CANfile_directory) + "**/*.asc", recursive=True)
    cansniff_files = glob.glob(str(processed_CANfile_directory) + "**/*.cansniff", recursive=True)

    data_dict = {}
    for x in image_folder_list:
        temp_dict = {}
        for y in cansniff_files:
            # print(x,y)
            if x in y:
                temp_dict['cansniff'] = y
        for y in asc_files:
            # print(x,y)
            if x in y:
                temp_dict['asc'] = y
        data_dict[x] = temp_dict

    data_dict2 = data_dict.copy()
    for item in data_dict:
        temp_dict1 = data_dict2[item]
        # print(data1['cansniff'])
        if bool(temp_dict1):
            if debug:
                print(temp_dict1)
        else:
            data_dict2.pop(item)
            if debug:
                print(f"popped {item}")

    info_list = []

    for i, folder in enumerate(data_dict2):
        file_log = []
        line_track = [0, 0, 0, 0]
        image_init = [0, 0, 0, 0]
        image_paths = list((Base_image_directory / folder).rglob('*.png'))  # List with all image absolute paths
        image_paths.sort()

        log_name = data_dict[folder]['asc']
        cansniff_name = data_dict[folder]['cansniff']
        with open(processed_CANfile_directory / cansniff_name, 'r') as snifffile:
            unix_timestamp = float(snifffile.readline().replace('// first time stamp: ', ''))
            if debug:
                print(unix_timestamp)

        lines = []
        date_data = []
        GPS_number = 0
        last_line = [0, 0, 0, 0]
        with open(processed_CANfile_directory / log_name, 'r') as myfile:
            for line in myfile:
                if line[2].isdigit():  # Makes sure that we are only reading data (ignoring headers)
                    lines.append(line.split())  # Add to the list with row data

        new_location = new_images_directory / folder
        if not os.path.isdir(new_location):
            print(f"Processing the files in {folder}")
            pt.Path(new_location).mkdir(parents=True, exist_ok=True)
            for img_num, image in enumerate(image_paths):
                image_name = image.name  # Extract image name as string
                image_data = image_name.replace('.png', '').split('_')
                image_time = float(image_data[-1])  # Extract image Unix time (-4 removes .png)
                camera_number = int(image_data[2])

                image_pil = Image.open(Base_image_directory / folder / image_name)
                brightness = calculate_brightness(image_pil)

                # Algorithm to find closest pair of numbers from timestamp
                current_num = 0.0
                latitude = 0
                longitude = 0
                GPS_message = 'NULL'

                # break

                # for j, line in enumerate(lines):
                for j in range(line_track[camera_number - 1], len(lines)):
                    line = lines[j]
                    if r'FEF3' in line[2][-7:-3]:
                        GPS_number = int(line[1])
                        GPS_message = line[2]
                        current_num = float(line[0]) + unix_timestamp
                        temp_number = int(camera_number) + GPS_offset
                        data_temp_line = [str(current_num)] + line[1:]
                        if temp_number == GPS_number:
                            if current_num >= image_time:
                                if image_init[camera_number - 1] == 0:
                                    # print(f"debug-{line_track[camera_number - 1]}")
                                    # latitude, longitude = find_long_and_lat(data_temp_line, [0], image_time)
                                    latitude, longitude = find_long_and_lat(line, [0], image_time, unix_timestamp)
                                    # print(latitude, longitude)
                                    last_line[camera_number - 1] = line
                                else:
                                    # latitude, longitude = find_long_and_lat(last_line[GPS_number], data_temp_line,
                                    #                                         image_time)
                                    latitude, longitude = find_long_and_lat(last_line[camera_number - 1], line,
                                                                            image_time
                                                                            , unix_timestamp)
                                    # print(latitude, longitude)
                                if debug:
                                    print(f"Camera {camera_number} with {GPS_number} has matched in line {j}.")
                                    print(f"Unix: {current_num}, Image Time:{image_time}, GPS Header: {line[2]}, "
                                          f"lat: {latitude}, long: {longitude}")
                                line_track[camera_number - 1] = j
                                # print(f"line track :{line_track[camera_number - 1]} - {last_line[camera_number - 1]}")
                                image_init[camera_number-1] = 1
                                # input("Press Enter to continue...")

                                break
                            else:
                                # last_line[GPS_number] = data_temp_line
                                last_line[camera_number - 1] = line
                    else:
                        continue

                if brightness > b_factor:
                    # print(f"{file}:{brightness}. Moving to target")
                    shutil.copy2(image, new_location / image_name)

                    image_new_name = image_name.replace('.png', '') + '_GPS_' + format(latitude, '.10f') + '_' + format(
                        longitude, '.10f') + '.png'

                    os.rename(new_location / image_name, new_location / image_new_name)

                    info = {'log name': log_name, 'image name': image_new_name, 'image timestamp': image_time,
                            'camera number': camera_number, 'latitude': format(latitude, '.10f'),
                            'longitude': format(longitude, '.10f'), 'GPS Header': GPS_message, 'GPS number': GPS_number}
                    info_list.append(info)
                    file_log.append(info)
                else:
                    print(f"{img_num}:{len(image_paths)} | Dark Image : {brightness}", end='\r')

            print(f'Saving report for {folder} at {report_directory / folder}.csv')
            temp_df = pd.DataFrame(file_log)
            temp_df.to_csv(report_directory / f'{folder}.csv')
        else:
            print(f"The folder {i} has already been processed.")

    df = pd.DataFrame(info_list)
    df.to_excel(Base_directory_test / f'{date_print}_FurrowVision_Dataset.xlsx', sheet_name='Full_report')
    print("------------End of Program:------------ \n")
