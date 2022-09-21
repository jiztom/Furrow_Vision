from lxml import etree
import pandas as pd
import pathlib as pt

if __name__ == '__main__':
    source = pt.Path(r'D:\Furrow Vision\PythonProject_Furrow\XML\TEst')
    destination = pt.Path(r'D:\Furrow Vision\PythonProject_Furrow\XML\Output')

    file = source / 'annotations.xml'
    root = etree.parse(file).getroot()
    anno = []
    whole_data = []
    user = root.findall('.//assignee/username')[0].text
    image_list = root.findall('image')
    for i, image in enumerate(image_list):
        image_info = image.items()
        child = image.getchildren()
        for label in child:
            label_data = dict(label.items())
            label_data.update(image_info)
            label_data.update({'user': user})
            for attrib in label.getchildren():
                temp = dict(attrib.items())
                label_data[temp['name']] = attrib.text
            whole_data.append(label_data)
    df = pd.DataFrame(whole_data)
    df.to_excel(destination / 'Extracted_data_andrea_test.xlsx')
    pass
