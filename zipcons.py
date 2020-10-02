import csv
import shutil
from collections import namedtuple
from io import BytesIO, StringIO
from multiprocessing.pool import Pool
from pathlib import Path
from typing import List
from zipfile import ZipFile
import xml.etree.cElementTree as ET

files_directory = Path("files")
cpu_count = 2

Level = namedtuple('Level', 'id level')
Object = namedtuple('Object', 'id object_name')


def _process_xml_data_pure(content):
    root = ET.fromstring(content)
    var_elems = root.findall('var')
    id_ = var_elems[0].get('value')
    level = var_elems[1].get('value')
    level = Level(id=id_, level=level)
    objects = []
    for objects_elem in root.findall('objects/object'):
        object_name = objects_elem.get('name')
        object_ = Object(id=id_, object_name=object_name)
        objects.append(object_)
    return level, objects


def _process_xml_data_c(content):
    import parsermodule
    id_, level = parsermodule.get_level(str(content, encoding='utf-8'))
    string_objects = parsermodule.get_objects(str(content, encoding='utf-8'))

    level = Level(id=id_, level=level)
    objects = [Object(id=id_, object_name=object_name) for object_name in string_objects.split()]
    return level, objects


def process_xml_data(content: bytes, optimization: bool = True) -> (Level, List[Object]):
    """
    :param content: bytes: content of a xml file
    :param optimization: if True use C extension for parsing else use etree.
    :returns level: Level namedtuple: contains data about level of the xml.
             objects: list of Object namedtuple: contains all object names
             that belong to the xml.
    """
    # C extension works 50% faster.
    if optimization:
        return _process_xml_data_c(content)
    return _process_xml_data_pure(content)


def process_archive(archive_path: Path) -> (List[Level], List[Object]):
    """
    Loads the archive into RAM, extracts data and returns it.
    :returns levels_data: list of Level namedtuple: contains data about level of
                          each xml in the specified archive.
             objects_data: list of Object namedtuple: contains all object names
                           that belong to the archive.
    """
    levels_data = []
    objects_data = []

    # Extract zipfile to in-memory files.
    bytesio_files = []
    with ZipFile(archive_path, 'r') as archive:
        for item in archive.filelist:
            content = archive.open(item)
            bytesio_file = BytesIO()
            bytesio_file.write(content.read())
            bytesio_files.append(bytesio_file)

    # Process xmls.
    for bytesio_file in bytesio_files:
        content = bytesio_file.getvalue()

        level, object_names = process_xml_data(content)
        levels_data.append(level)
        objects_data.extend(object_names)

    return levels_data, objects_data


def save_to_csv(levels_data: List[Level], objects_data: List[Object], output_directory=None) -> None:
    if not output_directory:
        output_directory = files_directory
    levels_filename = 'levels.csv'
    objects_filename = 'objects.csv'

    # Usage of in-memory StringIOs increases performance by 40%
    stringio_levels = StringIO()
    csv_writer = csv.writer(stringio_levels)
    for level_data in levels_data:
        csv_writer.writerow((level_data.id, level_data.level))

    stringio_objects = StringIO()
    csv_writer = csv.writer(stringio_objects)
    for object_data in objects_data:
        csv_writer.writerow((object_data.id, object_data.object_name))

    # Write to temp files first since the files might be big enough.
    # So we can save the data more reliable.
    # newline='' required since csv writes writes newline by itself.
    with open(output_directory / (levels_filename + '.tmp'), 'w', newline='') as csv_file:
        csv_file.write(stringio_levels.getvalue())
    with open(output_directory / (objects_filename + '.tmp'), 'w', newline='') as csv_file:
        csv_file.write(stringio_objects.getvalue())

    shutil.move(output_directory / (levels_filename + '.tmp'), output_directory / levels_filename)
    shutil.move(output_directory / (objects_filename + '.tmp'), output_directory / objects_filename)


def process_archives(dir_path: Path, parallelism: bool = True) -> None:
    """
    :param dir_path: Path: a directory with archives
    :param parallelism: if True use parallel calculations on different processes.
    """
    # Get the data.
    levels_data, objects_data = [], []
    entries = list(dir_path.iterdir())
    entries = filter(lambda e: e.name.endswith('.zip'), entries)  # Filter out all but zip archives.

    if parallelism:
        with Pool(cpu_count) as p:
            results = p.map(process_archive, entries)
        for r in results:
            levels_data.extend(r[0])
            objects_data.extend(r[1])
    else:
        for entry in entries:
            levels_archive_data, objects_archive_data = process_archive(entry)
            levels_data.extend(levels_archive_data)
            objects_data.extend(objects_archive_data)

    # Save the data to csv files.
    save_to_csv(levels_data, objects_data, dir_path)


def main():
    process_archives(files_directory)


if __name__ == '__main__':
    main()
