import os
import pathlib as pt
import shutil
import random
import math

source_folder = pt.Path(r'E:\Furrow\Label_data')

destination_folder = pt.Path(r'E:\Furrow\Split_Images')

batch_num = 100

all_lines = os.listdir(source_folder)
lines = random.sample(all_lines, len(all_lines))

div_val = float(math.ceil(len(lines)/batch_num))
i = 0
for img_count, image in enumerate(lines):
    if float(img_count) % div_val == 0:
        i += 1
    folder_name = f'Dataset_{i}'
    pt.Path(destination_folder / folder_name).mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_folder / image, destination_folder / folder_name / image)

