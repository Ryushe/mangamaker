import os
import subprocess 
from utils.utils import get_folder_files

def get_paths(dir, files):
    paths = []
    for file in files:
        paths.append(os.path.join(dir, file))
    return paths


def good_ol_metadata(book_data, kcc_tmp, covers_tmp, series):
    asin, publisher, publication_date, author, author_sort = book_data.values()
    print(f"editing metadata of {series}")

    kcc_files =  sorted(get_folder_files(kcc_tmp))
    cover_files = sorted(get_folder_files(covers_tmp))

    kcc_paths = get_paths(kcc_tmp, kcc_files)
    cover_paths = get_paths(covers_tmp, cover_files)

    # figure why no work
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
            print(f"file: {file} edited properly")
        except subprocess.CalledProcessError as e:
            print(f"file: {file} not edited properly")
    return kcc_paths