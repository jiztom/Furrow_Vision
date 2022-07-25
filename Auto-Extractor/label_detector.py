import os
import pathlib as pt
import subprocess

output_destination = r'Logger'
directory = pt.Path(r'T:\ftp\seeding\FurrowVision\MACHINE_DATA\FIELD_LOGS\2021_TDP\RAW_LOGS\MINNESOTA')
pre_processing = pt.Path(r'T:\ftp\seeding\FurrowVision\MACHINE_DATA\TEMPORARY\PreProcessing')

header = ['Field Name', 'Raw Log Location', 'Raw Log Count', 'Raw Log File Size', 'Logs Processed',
          'Extracted Log size',
          'Extraction status', 'Successful extraction', 'Failed Extraction']


def dir_empty(dir_path):
    return not any((True for _ in os.scandir(dir_path)))

# pathlist = Path(directory).glob('*.txt')
empty_list = []
missing_list = []
full_extraction = []
pre_processing_folder = pre_processing / directory.stem / directory.stem

os.chdir(directory)
with open(os.devnull, 'w') as FNULL:
    # print([Console, str(temp_path_str)])
    process = subprocess.Popen([r'powershell.exe',
                                r'C:\Users\abe_jiztom\Desktop\FielSize.ps1'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    print(f"Directory size = {out}")
    raw_log_size = out

for idx, path in enumerate(directory.glob('*.log'), start=1):
    temp = pt.Path(path)
    # print(temp.stem)
    extracted_path = pre_processing_folder / temp.stem
    try:
        if dir_empty(extracted_path):
            # print("Added sucessfully.")
            empty_list.append(path)
        else:
            full_extraction.append(path)
    except:
        print(f"The following file {extracted_path} is missing.")
        missing_list.append(path)
    # print(path)
print(idx)
list = [directory.stem, directory, idx, raw_log_size, len(empty_list) + len(full_extraction), missing_list]
print(list)
