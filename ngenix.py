from timeit import default_timer

import zipcons
import zipgen


def main():
    # 1. Generate Zips with Xmls.
    zipgen.main()
    # 2. Process Zips with Xmls saving data to Csv files.
    start = default_timer()
    zipcons.main()
    end = default_timer()
    print(f"CSV files have been saved to {zipcons.files_directory.absolute()}.")
    print(f"Processing time: {(end - start) * 1e3} ms")


if __name__ == '__main__':
    main()
