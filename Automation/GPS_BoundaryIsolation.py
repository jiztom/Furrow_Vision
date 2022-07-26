import shutil

import fiona
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import pathlib as pt
import os

filename = pt.Path(r'D:\Furrow Vision\PythonProject_Furrow\Data\Shapefiles\GCP_polygon\GCPs_polygon.shp')

folder = pt.Path(r'F:\GPSProcessed')
destination = pt.Path(r'F:\CroppedData')
shape_file = fiona.open(filename)
print(shape_file.schema)

poly_list = []
iter1 = iter(shape_file)
for i in range(len(shape_file)):
    # first = next(iter(shape_file))
    # first = shape_file.next()
    first = next(iter1)
    cord = first['geometry']['coordinates'][0]
    print(cord)

    x, y = [], []
    for elem in cord:
        x.append(elem[0])
        y.append(elem[1])

    plt.scatter(x, y)
    plt.show()

    poly_cord = Polygon(cord)
    poly_list.append(poly_cord)

# folder_list = os.listdir(folder)
#
# for i, folder_name in enumerate(folder_list):
#     # print(f'Running for {folder_name}')
#     image_list = os.listdir(folder / folder_name)
#     count = 0
#     for image in image_list:
#         image_name = image.replace('.png', '').split('_')
#         frame_number = int(image_name[4])
#         point1 = Point(float(image_name[-1]), float(image_name[-2]))
#
#         if point1.within(poly_cord):
#             # print(f'Moving {image} from {folder_name}')
#             if frame_number % 2 == 1:
#                 count += 1
#                 pt.Path(destination / folder_name).mkdir(parents=True, exist_ok=True)
#                 shutil.copy2(folder / folder_name / image, destination / folder_name / image)
#     print(f'Moved {count}/{len(image_list)} from {folder_name}')
