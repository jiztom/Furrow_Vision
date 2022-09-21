import os
import sys
from PIL import Image
import pathlib as pt
import shutil

source = pt.Path(r'E:\Furrow\Label_data')
destination = pt.Path(r'E:\Furrow\Rotated')

image_list = os.listdir(source)

for i, file in enumerate(image_list):
    image = Image.open(source / file)
    image_rotate = image.rotate(180)
    image_rotate.save(destination / file)
    print(f"Running {i}:{len(image_list)}", end='\r')
