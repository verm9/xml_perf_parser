import shutil
from pathlib import Path
from zipfile import ZipFile

import pytest

from zipgen import generate_xmls_content, generate_zips


files_directory = Path("testfiles")


@pytest.fixture(scope='function')
def setup_files_directory(request):
    files_directory.mkdir(parents=True, exist_ok=True)

    def some_teardown():
        shutil.rmtree(files_directory)
    request.addfinalizer(some_teardown)

    return None


def test_generate_xmls_content():
    contents = list( generate_xmls_content() )
    assert len(contents) == 100


def test_generate_zips(setup_files_directory):
    num_of_archives = 10
    generate_zips(files_directory, num_of_archives)

    assert len( list(files_directory.iterdir()) ) == num_of_archives

    # Check whats inside.
    archive_path = next(files_directory.iterdir())
    with ZipFile(archive_path, 'r') as archive:
        for item in archive.filelist:
            assert item.filename.endswith('xml')
