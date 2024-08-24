import os
import subprocess 
from utils.utils import get_folder_files

def get_paths(dir, files):
    # D:\\Code\\Python\\mangamaker\\.tmp\\.tmp_covers\\, gantz_c101_c150.jpg
    paths = []
    for file in files:
        paths.append(os.path.join(dir, file))
    return paths


def apply(input_directory, covers_tmp, series, book_data =''):
    print(f"editing metadata of {series}")

    input_files = sorted(get_folder_files(input_directory))
    cover_files = sorted(get_folder_files(covers_tmp))

    # figure why no work
    for file, cover in zip(input_files, cover_files):
        if book_data:
            asin, publisher, publication_date, author, author_sort = book_data.values()
            command = ("ebook-meta"
                    f" {file}"
                    f" --identifier amazon:{asin}"
                    f" --publisher '{publisher}'"
                    f" --date '{publication_date}'"
                    f" --cover {cover}"
                    f" --authors '{author}'"
                    f" --author-sort '{author_sort}'"
                    f" --series '{series}'")
        else: # defaults to only cover
            command = ("ebook-meta"
                    f" {file}"
                    f" --cover {cover}"
                    f" --series '{series}'")
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"file: {file} edited properly")
        except subprocess.CalledProcessError as e:
            print(f"file: {file} not edited properly")
    # return kcc_paths

