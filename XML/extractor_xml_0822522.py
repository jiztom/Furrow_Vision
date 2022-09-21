# %%
import os

import argparse
import shutil
import numpy as np
from lxml import etree
from tqdm import tqdm
import pandas as pd
import pathlib as path
import datetime

list = ['id', 'image count', 'name', 'width', 'height', 'shapes', 'user', 'source', 'seed number', 'Seed_points', 'xmin'
        ,'ymin', 'xmax', 'ymax', 'Trainable', 'Residue occlusion', 'Seed tip (Pitch)', 'Seed germ (Roll)', 'Seed tip',
        'Seed Type', 'Trench_points', 'Is trench collapsed', 'Shallow seeding depth', 'Residue in trench']


image_count = 0


def dir_create(path):
    if (os.path.exists(path)) and (os.listdir(path) != []):
        shutil.rmtree(path)
        os.makedirs(path)

    if not os.path.exists(path):
        os.makedirs(path)


def parse_anno_file(cvat_xml, image_name, folder, temp_location, source):
    global image_count
    root = etree.parse(cvat_xml).getroot()
    anno = []
    whole_data = []
    image_name_attr = ".//image[@name='{}/{}']".format(temp_location, image_name)
    image = {}
    image = dict.fromkeys(list)
    for image_tag in root.iterfind(image_name_attr):
        image_count += 1
        # image = dict.fromkeys(list)

        for key, value in image_tag.items():
            image[key] = value

        image['shapes'] = []
        seed = 0

        for tag_label in image_tag.iter('tag'):
            tag = {'type': 'tag'}
            temp = ''
            for key, value in tag_label.items():
                tag[key] = value
            test = {}
            for attrib in tag_label.iter('attribute'):
                temp = ''
                for key, value in attrib.items():
                    # test[key] = value
                    temp = value
                image[temp] = attrib.text
            image['shapes'].append(tag)
            image['shapes'].sort(key=lambda x: int(x.get('z_order', 0)))

        for box_tag in image_tag.iter('box'):
            image['image count'] = image_count
            image['user'] = folder
            image['source'] = source
            box = {'type': 'box'}
            temp_points = ''
            for key, value in box_tag.items():
                box[key] = value
            if box['label'] == 'Seed':
                seed = seed + 1
                image['seed number'] = seed

            temp_points = box['label'] + f'_points'
            if temp_points in image:
                # temp_points = box['label'] + f'_points_{seed}'
                temp_points = box['label'] + f'_points'

            image[temp_points] = "{0},{1};{2},{1};{2},{3};{0},{3}".format(box['xtl'], box['ytl'], box['xbr'],
                                                                          box['ybr'])
            image['xmin'] = box['xtl']
            image['ymin'] = box['ytl']
            image['xmax'] = box['xbr']
            image['ymax'] = box['ybr']

            # test = {}
            for attrib in box_tag.iter('attribute'):
                temp = ''
                for key, value in attrib.items():
                    # test[key] = value
                    temp = value
                image[temp] = attrib.text
                # print(test)
                # boc_temp.append(test)
            # image['seed count'] = seed
            # box_list.append(test)
            image['shapes'].append(box)

            if box['label'] == 'Seed':
                anno.append(image)
                # temp_seed += 1
                image = {}
                for key, value in image_tag.items():
                    image[key] = value
                image['shapes'] = []
            whole_data.append(image)
    return anno, image , whole_data


class ArgumentTemp:
    image_dir = path.Path(r'D:\Machine Learning\Digital Acre\Data_2')
    scale_factor = 1.0


# temp_anno, test1 = main()

temp_anno = []
test1 = []
whole = []
args = ArgumentTemp()
# dir_create(args.output_dir)

folders = [f for f in os.listdir(args.image_dir)]

global_counter = 0
for folder in folders:
    # image_folder = args.image_dir / folder / 'images' / 'Images_Bulk_Labeling'
    image_folder = args.image_dir / folder / 'images'
    image_folder = [x[0] for x in os.walk(image_folder)][-1]
    # print(image_folder)
    temp_location = os.sep.join(image_folder.rsplit('\\')[-2:]).replace('\\', '/')
    source_folder = args.image_dir / folder / 'images'
    cvat_file = str(args.image_dir / folder / 'annotations.xml').replace('\\', '/')
    img_list = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    for img in tqdm(img_list, desc=f'Extracting Annotations for {folder}:\t'):
        anno, image1, whole_data = parse_anno_file(cvat_file, img, folder, temp_location, source_folder)
        temp_anno.extend(anno)
        test1.append(image1)
        whole.extend(whole_data)
    global_counter = global_counter + 1

df_test = pd.DataFrame(temp_anno)
df = pd.DataFrame(test1)
# # df.to_csv('Data_01072022.csv')
# # df.to_excel('Data.xlsx')
datetime_object = datetime.datetime.now()
date_time_clean = datetime_object.strftime('%m%d%Y_%H%M%S')
df_test.to_excel(f'SingleSeed_{date_time_clean}.xlsx')

df_whole = pd.DataFrame(whole)
df_whole.to_excel(f'WholeData_{date_time_clean}.xlsx')

