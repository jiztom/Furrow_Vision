import pandas as pd
import pathlib as pt

source_folder = pt.Path(r'T:\current\Projects\Deere\CPSI\2022\Digital Acre\2022_GPSProcessedData\Rot_split_image')

result = list(source_folder.rglob("*.[pP][nN][gG]"))

# data = {}
data_all = []

for l, val in enumerate(result):
    temp = pt.Path(val)
    data = {}
    data['Image Filename'] = temp.name
    data['Source Folder'] = temp.parent
    data['Folder'] = temp.parents[0].stem
    print(f'{data}')
    data_all.append(data)

df = pd.DataFrame(data_all)
destination = pt.Path(r'T:\current\Projects\Deere\CPSI\2022\Digital Acre\2022_GPSProcessedData')
df.to_csv(destination / 'LabelExtract.csv')
