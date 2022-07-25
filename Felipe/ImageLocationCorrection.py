# Goals of the script

import pandas as pd
import csv
import math
import pandas as pd
import pathlib as pt
import os

Data_directory = pt.Path(r'C:\Users\abe_felipec\PycharmProjects\da-isu\DataWranglingScripts')
data = pd.read_csv(os.path.join(Data_directory, "ImageData_DigitalAcre_Treatments.csv"))

data_list = []
for index, row in data.iterrows():
    LogName = row["Log Name"]
    imageName = row["Image Name"]
    cameraNumber = row['Camera Number']
    latitude = row["Latitude"]
    longitude = row["Longitude"]

    new_longitude = longitude + 0.0000027
    new_latitude = latitude + 0.0000017

    info = [LogName, imageName, cameraNumber, new_longitude, new_latitude]
    data_list.append(info)

with open('ImageData_Aligned.csv', 'w', encoding='UTF8', newline='') as file:
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    # Header
    wr.writerow(['Log Name', 'Image Name', 'Camera Number', 'Longitude', 'Latitude'])
    # Write data
    wr.writerows(data_list)
