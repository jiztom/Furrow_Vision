import csv
import math
import pandas as pd
import pathlib as pt
import os

# Points to the directory where excel/CSV files are located
Data_directory = pt.Path(r'C:\Users\abe_felipec\PycharmProjects\da-isu\DataWranglingScripts')

# Resolution of desired image
image_resolution = [1086, 1448]
# Image center point is half of the total vertical and horizontal resolution
image_center_point = [image_resolution[0] / 2, image_resolution[1] / 2]

# Conversion from inches to pixels
in_per_pixel = 0.0069

# One inch corresponds to a certain value in Latitude in Ames - Iowa
one_inch_in_lat = 2.2875 * (10 ** -7)

# One inch corresponds to a certain value in Lonj.,gitude in Ames - Iowa
one_inch_in_lon = 3.06725837 * (10 ** -7)


# Points come is format point = pixelX, pixelY
# Returns pixel location of center of the square
def get_center_of_square(coords):

    a = []
    for i in range(len(coords)):
        a.append(coords[i].split(','))
    mid_pixel = [0] * 2
    mid_pixel[0] = round((float(a[0][0]) + float(a[1][0])) / 2)
    mid_pixel[1] = round((float(a[0][1]) + float(a[3][1])) / 2)
    return mid_pixel


def get_x_y_shift_two_points(p1, p2):
    xy_shift = [0] * 2
    xy_shift[0] = p1[0] - p2[0]
    xy_shift[1] = p1[1] - p2[1]
    return xy_shift


def pixel_to_in(pixel_distance):
    return round(pixel_distance * in_per_pixel, 4)


def find_GPS_of_pixel(pixel_translate, reference_latitude, reference_longitude):
    lat_difference = pixel_translate[1] * one_inch_in_lat
    lon_difference = pixel_translate[0] * one_inch_in_lon
    new_lat = reference_latitude - lat_difference
    new_lon = reference_longitude + lon_difference
    return new_lon, new_lat


def isNaN(num):
    return num != num


def align(seed_points, lat, lon):
    if not isNaN(seed_points):
        points = seed_points.split(';')
        center_seed = get_center_of_square(points)
        pixel_shift = get_x_y_shift_two_points(center_seed, image_center_point)
        pixel_shift[0] = pixel_to_in(pixel_shift[0])
        pixel_shift[1] = pixel_to_in(pixel_shift[1])
        seed_align_location = find_GPS_of_pixel(pixel_shift, lat, lon)
        # input("__Press any key to continue and press enter__\n")  # For testing purposes
        return seed_align_location
    else:
        return 0


# Read in Data from Excel sheet
data = pd.read_csv(os.path.join(Data_directory, "Complete_Dataset_V6_YieldCalcs_JoinFV01312022.csv"))
data_list = []
counter = 0
for index, row in data.iterrows():
    seed_points_1 = row['Seed_points']
    seed_points_2 = row['Seed_points_2']
    seed_points_3 = row['Seed_points_3']
    seed_points_4 = row['Seed_points_4']
    latitude = row['FVImageLatitude']
    longitude = row['FVImageLongitude']

    seed_location = align(seed_points_1, latitude, longitude)
    if seed_location != 0:
        counter = counter + 1
        info = [counter, row['name'], seed_location[0], seed_location[1]]
        data_list.append(info)

    seed_location = align(seed_points_2, latitude, longitude)
    if seed_location != 0:
        counter = counter + 1
        info = [counter, row['name'], seed_location[0], seed_location[1]]
        data_list.append(info)

    seed_location = align(seed_points_3, latitude, longitude)
    if seed_location != 0:
        counter = counter + 1
        info = [counter, row['name'], seed_location[0], seed_location[1]]
        data_list.append(info)

    seed_location = align(seed_points_4, latitude, longitude)
    if seed_location != 0:
        counter = counter + 1
        info = [counter, row['name'], seed_location[0], seed_location[1]]
        data_list.append(info)


with open('SeedData_02032022.csv', 'w', encoding='UTF8', newline='') as file:
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    # Header
    wr.writerow(['Seed ID', 'Image Name', 'Longitude', 'Latitude'])
    # Write data
    wr.writerows(data_list)
