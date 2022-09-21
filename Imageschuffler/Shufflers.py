import os
import pathlib as pt
import shutil
import random
import math

source_folder = pt.Path(r'E:\Furrow\Rotated')

destination_folder = pt.Path(r'E:\Furrow\Split_Images_rot')

batch_num = 1000

all_lines = os.listdir(source_folder)
lines = random.sample(all_lines, len(all_lines))

div_val = float(math.floor(len(lines)/batch_num))
# div_val = 50
i = 0
for img_count, image in enumerate(lines):
    if float(img_count) % div_val == 0:
        i += 1
    # if i ==2:
    #     break
    folder_name = f'Dataset_{i}'
    print(f'Processing {img_count}:{len(lines)}')
    pt.Path(destination_folder / folder_name).mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_folder / image, destination_folder / folder_name / image)


print("Transfer Completed.")
