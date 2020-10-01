import shutil
from pathlib import Path
import pytest

from zipcons import process_archives
from zipgen import generate_zips

files_directory = Path("testfiles")


@pytest.fixture(scope='function')
def setup_files_directory_with_archives(request):
    files_directory.mkdir(parents=True, exist_ok=True)
    generate_zips(files_directory, 10)

    def some_teardown():
        shutil.rmtree(files_directory)
    request.addfinalizer(some_teardown)

    return None


def test_process_archives(setup_files_directory_with_archives):
    process_archives(files_directory)

    # Count num of lines. Default 100 per xml is assumed.
    with open(files_directory / "levels.csv") as csv_file:
        lines_num = sum(1 for _ in csv_file.readlines())
    assert lines_num == 1000
