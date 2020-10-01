import zipfile
import random
import string
import xml.etree.cElementTree as ET
from io import BytesIO
from pathlib import Path
from uuid import uuid4

files_directory = Path("files")


def check_dirs():
    files_directory.mkdir(parents=True, exist_ok=True)


def get_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters, k=length))


def generate_xmls_content(num=100, beautify=False):
    if beautify:
        import vkbeautify

    result = []
    for i in range(num):
        root = ET.Element("root")
        ET.SubElement(root, "var", name="id", value=str(uuid4()))
        ET.SubElement(root, "var", name="level", value=str(random.randint(1, 100)))

        objects = ET.SubElement(root, "objects")
        for _ in range(random.randint(1, 10)):
            ET.SubElement(objects, "object", name=get_random_string())

        xml_text = ET.tostring(root, encoding='unicode')
        if beautify:
            xml_text = vkbeautify.xml(xml_text)  # return String, non-std lib
        result.append(xml_text)
    return result


def generate_zips(directory: Path = None, num=50):
    if not directory:
        directory = files_directory
    for i in range(num):
        xmls_content = generate_xmls_content()

        # This is where the zip will be written.
        buff = BytesIO()
        # This is the zip file.
        zip_archive = zipfile.ZipFile(buff, mode='w')

        for j, content in enumerate(xmls_content):
            bytesio_xml = BytesIO()
            bytesio_xml.write(bytes(content, 'utf-8'))
            zip_archive.writestr(f"filename_{j}.xml", bytesio_xml.getvalue())
        # Here you finish editing your zip. Now all the information is
        # in your buff BytesIO object.
        zip_archive.close()

        with open(directory / f'archive_{i}.zip', 'wb') as f:
            f.write(buff.getvalue())


def main():
    check_dirs()
    generate_zips()


if __name__ == '__main__':
    main()
