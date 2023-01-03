# %%
import os

import argparse
import shutil
import numpy as np
from lxml import etree
from tqdm import tqdm
import pandas as pd
import pathlib as path

string = ['SET3', 'SET5', 'SET1', 'SET2', 'SET4', 'MiniSET4', 'MiniSET5', 'MiniSET2', 'MiniSET3', 'MiniSET1',
          'SET7', 'SET6']


def dir_create(path):
    if (os.path.exists(path)) and (os.listdir(path) != []):
        shutil.rmtree(path)
        os.makedirs(path)

    if not os.path.exists(path):
        os.makedirs(path)


def parse_args():
    parser = argparse.ArgumentParser(
        fromfile_prefix_chars='@',
        description='Convert CVAT XML annotations to CSV'
    )
    parser.add_argument(
        '--image-dir', metavar='DIRECTORY', required=True,
        help='directory with input images'
    )
    parser.add_argument(
        '--cvat-xml', metavar='FILE', required=True,
        help='input file with CVAT annotation in xml format'
    )
    parser.add_argument(
        '--output-dir', metavar='DIRECTORY', required=True,
        help='directory for output masks'
    )
    parser.add_argument(
        '--scale-factor', type=float, default=1.0,
        help='choose scale factor for images'
    )
    return parser.parse_args()


def parse_anno_file(cvat_xml, image_name, folder, global_counter):
    root = etree.parse(cvat_xml).getroot()
    anno = []
    if 4 < global_counter < 10:
        image_name_attr = ".//image[@name='Images_Bulk_labelling_mini/" + string[global_counter] + "/{}']".format(image_name)
    else:
        image_name_attr = ".//image[@name='Images_Bulk_Labeling/" + string[global_counter] + "/{}']".format(image_name)

    for image_tag in root.iterfind(image_name_attr):
        image = {}
        image['user'] = folder
        for key, value in image_tag.items():
            image[key] = value

        image['shapes'] = []
        seed = 0
        for box_tag in image_tag.iter('box'):
            box = {'type': 'box'}
            temp_points = ''
            for key, value in box_tag.items():
                box[key] = value

            if box['label'] == 'Seed':
                seed += 1
            temp_points = box['label'] + f'_points'
            if temp_points in image:
                temp_points = box['label'] + f'_points_{seed}'

            image[temp_points] = "{0},{1};{2},{1};{2},{3};{0},{3}".format(box['xtl'], box['ytl'], box['xbr'],
                                                                          box['ybr'])
            test = {}
            for attrib in box_tag.iter('attribute'):
                temp = ''
                for key, value in attrib.items():
                    # test[key] = value
                    temp = value
                image[temp] = attrib.text
                # print(test)
                # boc_temp.append(test)
            image['seed count'] = seed
            # box_list.append(test)
            image['shapes'].append(box)

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
        anno.append(image)
    return image


def main():
    # global args
    # args = parse_args()
    temp_anno = []
    args = ArgumentTemp()
    # dir_create(args.output_dir)

    folders = [f for f in os.listdir(args.image_dir)]

    global_counter = 0
    for folder in folders:
        image_folder = args.image_dir / folder / 'images' / 'Images_Bulk_Labeling' / string[global_counter]
        cvat_file = str(args.image_dir / folder / 'annotations.xml').replace('\\', '/')
        img_list = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        for img in tqdm(img_list, desc=f'Extracting Annotations for {folder}:'):
            img_path = image_folder / img
            anno = parse_anno_file(cvat_file, img, folder, global_counter)
            temp_anno.append(anno)
        global_counter = global_counter + 1
    return temp_anno


class ArgumentTemp:

    # image_dir = path.Path(r'C:\Users\abe_felipec\Desktop\Annotations\Unzipped')
    image_dir = path.Path(r'T:\current\Projects\Deere\CPSI\2021\Digital Acre\DigitalAcre_DataSet_11302021\DigitalAcre_DataSet')
    # cvat_xml = r'D:\Jiztom\Machine Learning Practice\imageautolabeller\Code\Data Extraction\Training_jiztom\annotations.xml'
    # output_dir = path.Path(r'C:\Users\abe_felipec\Desktop\Data')
    scale_factor = 1.0


temp = main()
df = pd.DataFrame(temp)
df.to_csv('Data_11012022.csv')
df.to_excel('Data_11012022.xlsx')
