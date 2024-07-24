import os
import subprocess 
from utils.utils import get_folder_files

def get_paths(path, files):
    paths = []
    for file in files:
        paths.append(os.path.join(path, file))
    return paths


def good_ol_metadata(book_data, kcc_tmp, covers_tmp, series):
    print(book_data)
    asin, publisher, publication_date, author, author_sort = book_data.values()


    kcc_files =  sorted(get_folder_files(kcc_tmp))
    cover_files = sorted(get_folder_files(covers_tmp))

    kcc_paths = get_paths(kcc_tmp, kcc_files)
    cover_paths = get_paths(covers_tmp, cover_files)

    # figure of if work
    for file, cover in zip(kcc_paths, cover_paths):
        command = ("ebook-meta"
                   f" {file}"
                   f" --identifier amazon:{asin}"
                   f" --publisher '{publisher}'"
                   f" --date '{publication_date}'"
                   f" --cover {cover}"
                   f" --authors '{author}'"
                   f" --author-sort '{author_sort}'"
                   f" --series '{series}'")
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Calibre exited with {e}") 
    return kcc_paths