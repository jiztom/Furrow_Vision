# Goals of the script
# 1) Eliminate same seed in two different images
# 2) Micro adjust seed location to Sentera location
# 3) Apply correct Furrow Vision ID

import pandas as pd
import csv
import math
import pandas as pd
import pathlib as pt
import os

Data_directory = pt.Path(r'C:\Users\abe_felipec\PycharmProjects\da-isu\DataWranglingScripts')
data = pd.read_csv(os.path.join(Data_directory, "SeedData.csv"))

data_list = []
for index, row in data.iterrows():
    seedID = row["Seed ID"]
    imageName = row["Image Name"]
    longitude = row["Longitude"]
    latitude = row["Latitude"]

    new_longitude = longitude + 0.0000027
    new_latitude = latitude + 0.0000017

    info = [seedID, imageName, new_longitude, new_latitude]
    data_list.append(info)

with open('SeedData_Aligned.csv', 'w', encoding='UTF8', newline='') as file:
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    # Header
    wr.writerow(['Seed ID', 'Image Name', 'Longitude', 'Latitude'])
    # Write data
    wr.writerows(data_list)