from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import datetime
import os


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def save_XML(fileloc, extrLoc, imextXML, Console, proces_multi, datecreated):
    # print("point1")
    generated_on = str(datetime.datetime.now())
    top = Element('Extractor')
    # tree = ElementTree(top)
    top.set('version', '1.0.1')

    comment = Comment('Generated for ImageExtractor using machine')
    top.append(comment)
    head = SubElement(top, 'head')

    # print("point2")

    title = SubElement(head, 'title')
    title.text = 'Parameters'
    dc = SubElement(head, 'dateCreated')
    dc.text = datecreated
    dm = SubElement(head, 'dateModified')
    dm.text = generated_on

    source = SubElement(top, 'Source')
    source.text = fileloc

    destination = SubElement(top, 'Destination')
    destination.text = extrLoc

    # print("point3")

    xml = SubElement(top, 'XML')
    xml.text = imextXML

    # name_format_1 = SubElement(top, 'name_format')
    # name_format_1.text = name_format

    console = SubElement(top, 'ConsolePlayer')
    console.text = Console

    # print("point4")

    process = SubElement(top, 'multi')
    process.text = str(proces_multi)

    # print(prettify(top))
    data = prettify(top)

    # text_file = open(r"C:\Users\jiztom\Desktop\Python_Projects\ImageExtractor\parameters.xml", "wt")
    text_file = open(r"parameters.xml", "wt")
    text_file.write(data)
    text_file.close()


if __name__ == "__main__":
    generated_on = str(datetime.datetime.now())
    fileloc = r"T:\ftp\sprayers\IntelligentSprayTechnology\Connor_Field_Data\2020_ImageLibrary_FieldLogs_Jabil\2020" \
              r"-10-28_IA_FallowSoybeanResidue44vs30 "
    extrLoc = r"\\iastate\lss\research\darr-lab\current\Users\Staff\Jiztom\Python_Projects\Image_Extraction_Template" \
              r"\Test "
    name_format = r"%ID_%FN_%TS_%GT_%IN_%SN_%ST_%GN"
    Console = r"C:\Program Files\SeeAndSprayWorkbench\bin\ConsolePlayer.exe"
    imextXML = r"RoboticsWorkBench_image extractor.xml"
    process = r"2"
    date_created = generated_on
    save_XML(fileloc, extrLoc, imextXML, name_format, Console, process, date_created)
