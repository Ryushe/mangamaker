#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile

'''
This script is designed to convert .zip files downloaded from mangakatana.com into a series
of .cbz files. Each .zip file typically contains 10 chapters of the same manga stored as
a series of folders.
'''

def main():
    # Get the current script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    root_directory = script_directory

    # Iterate through the .zip files in the root directory
    for zip_file in os.listdir(root_directory):
        if zip_file.endswith(".zip"):
            zip_path = os.path.join(root_directory, zip_file)

            # Extract the chapter name from the .zip file name
            chapter_name = os.path.splitext(zip_file)[0]
            series_name = "-".join(chapter_name.split("_")[:-2])

            cbz_directory = os.path.join(root_directory, "cbz_files")
            if not os.path.exists(cbz_directory):
                os.makedirs(cbz_directory)

            try:
                cbz_count = 0
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for subfolder in zip_ref.namelist():
                        if subfolder.endswith('/') and subfolder != chapter_name + "/":
                            cbz_count += 1
                            subfolder_name = os.path.basename(subfolder[:-1])
                            cbz_path = os.path.join(cbz_directory, f"{series_name}_{subfolder_name}.cbz")

                            with zipfile.ZipFile(cbz_path, 'w', compression=zipfile.ZIP_DEFLATED) as cbz:
                                for file_in_zip in zip_ref.namelist():
                                    if file_in_zip.startswith(subfolder):
                                        file_content = zip_ref.read(file_in_zip)
                                        cbz_file_path = os.path.join(subfolder_name, os.path.basename(file_in_zip))
                                        cbz.writestr(cbz_file_path, file_content)
                print(f"ZIP processing completed: {chapter_name}.zip, {cbz_count} CBZ files generated, total: {len(os.listdir(cbz_directory))}")

            except Exception as e:
                print(f"Error while reading the ZIP file: {zip_path}\n{e}")

    print("Done!")

if __name__ == "__main__":
    main()
