import os
import subprocess 
from utils.utils import get_folder_files

def good_ol_metadata(book_data, kcc_tmp, cover_folder):
    print(book_data)
    asin, publisher, publication_date, author, author_sort = book_data.values()


    kcc_files =  sorted(get_folder_files(kcc_tmp))
    cover_files = sorted(get_folder_files(cover_folder))

    for file, cover in zip(kcc_files, cover_files):
        command = ("ebook-meta"
                   f" {file}"
                   f" --identifier amazon:{asin}"
                   f" --publisher {publisher}"
                   f" --date {publication_date}"
                   f" --cover {cover}"
                   f" --authors {author}"
                   f" --author-sort {author_sort}")
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Calibre exited with {e}") 
    return kcc_files