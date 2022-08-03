import pandas as pd
import pathlib as pt
import glob

# Choose what type of file you working with
file_type = 'CSV'  # 'EXCEL'/'CSV'

# change to the required folder destination
report_directory = pt.Path(r'F:\Reports')

# Location of output file
output_folder = pt.Path(r'F:')

# Output file name
output_file_name = r'Overall_merged_data_07-26'

# ----------------------------------------------------------------------------------------------------------
if file_type == 'EXCEL':
    data_files = glob.glob(str(report_directory) + "**/*.xlsx", recursive=True)
    destination = output_folder / f'{output_file_name}.xlsx'
elif file_type == 'CSV':
    data_files = glob.glob(str(report_directory) + "**/*.csv", recursive=True)
    destination = output_folder / f'{output_file_name}.csv'
else:
    data_files = glob.glob(str(report_directory) + "**/*.csv", recursive=True)
    destination = output_folder / f'{output_file_name}.csv'

data_list = []

for file in data_files:
    if file_type == 'EXCEL':
        data = pd.read_excel(file)
    elif file_type == 'CSV':
        data = pd.read_csv(file)
    else:
        data = pd.read_csv(file)
    data_list.append(data)

result = pd.concat(data_list)
result.latitude.fillna(result.lattitude, inplace=True)
result.drop('lattitude', axis=1, inplace=True)

if file_type == 'EXCEL':
    result.to_excel(destination)
else:
    result.to_csv(destination)
