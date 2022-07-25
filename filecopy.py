import os
import pathlib as pt
import glob
import shutil as sh
import time

# Initializing variables
camera_images = [0, 0, 0, 0]

# starting time
code_start = time.time()

# Hardcoding the values of input and output
source = pt.Path(r"T:\ftp\seeding\FurrowVision\MACHINE_DATA\TEMPORARY\Output\Minnesota\Automation")
dest = pt.Path(r'T:\ftp\seeding\FurrowVision\MACHINE_DATA\IMAGES\TEST_LOGS\2021_TDP\MINNESOTA')

# Creating list of log files in the destination
files = glob.glob(str(source).replace('\\', '/') + r'\**\*.png', recursive=True)

# Image transfer begin
# starting time
image_start = time.time()
for idx, file in enumerate(files):
    # Creating the destination and related location of the file to be processed
    temp = pt.Path(file)
    file_reduction = temp.stem.replace('furrow_vision', '')
    filename = str(temp.parent).split('\\')[-1] + file_reduction + '.png'
    camera = str(file).split('_')[-2]

    # Image relocation tracker
    camera_images[int(camera)] += 1

    camera_folder = 'CAMERA_'+ camera
    destination = dest / camera_folder / filename

    # File Copy constructor
    try:
        sh.copyfile(src=file, dst=destination)
    except:
        print(f'File copy for {filename} has failed due to some error.')

    print(f'Currently processing image number : {idx+1} \tCurrent camera images = {camera_images}')

# End time
end = time.time()

print(f'Final Results\n-----------------------------------------------')
print(f'No of images extracted : {len(files)}')
for i in range(4):
    print(f" Camera_{i+1} : {camera_images[i]}")
print('---------------------------------------------------------------')
