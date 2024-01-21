import git
import re
import subprocess
import patoolib
import os
import shutil
import time
import argparse


# useless rn 
def zip_to_cbz():
    if not os.path.isdir('cbz_files'):
        process = subprocess.Popen(["python", "make_cbz_out_of_zip.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if "Done!" in stdout:
            print("Process has finished successfully.")
        else:
            print(f"Process failed. Output:\n{stdout}\nError:\n{stderr}")

    else:
        print("cbz_files exists")
        print("Deleting cbz_files")
        try:
            shutil.rmtree('cbz_files')
        except:
            print("Failed to delete cbz all together")
        print("Trying to create cbz_files")
        zip_to_cbz()


def make_tempdir(dirname):
    try:
        print(f"attempting to create tempdir {dirname}")
        temp_dir = os.path.join(os.getcwd(), dirname)
        os.mkdir(temp_dir)
    except FileExistsError:
        print(f"dir {dirname} already exists (no biggie)")
    return temp_dir


def extract(archives_path): 

    temp_dir = make_tempdir('.tmp')

    # for file in archive(defualt) folder extract to .tmp
    for file in os.listdir(archives_path):
    # if not a folder
        file_check_path = os.path.join(archives_path, file)
        if os.path.isfile(file_check_path):
            try:
                patoolib.extract_archive(os.path.join(archives_path, file), outdir=temp_dir)
            except: 
                print("these files already exist")


# renames and moves all .jpg files in tmp
def handle_img_files():
    filename_count = 0
    tmp_directory = os.path.join(os.getcwd(), '.tmp') # tmp created in extract()
    files_good = True

    # for folder in .tmp do..
    for folder in os.listdir(tmp_directory):
        folder_path = os.path.join(tmp_directory, folder)
        # check if is folder in .tmp
        if os.path.isdir(folder_path):
            # for file in the folder
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                print(f"Working on file:\n{file_path}")
                if os.path.isfile(file_path) and file_path.endswith(".jpg"):
                    try:
                        new_filename = f"{filename_count}.jpg"
                        new_filepath = os.path.join(tmp_directory, f"{filename_count}.jpg") # .tmp + new_filename

                        new_filename = os.path.join(folder_path, new_filename)
                        # print(f"Renaming: {file}")
                        os.rename(file_path, new_filename)
                        filename_count += 1

                        # moves jpg files in folders -> tmp
                        move_jpg_tmp(new_filename, new_filepath)
                    
# could add a rerun feature if failed
                    except:
                        print("file {file} could't be renamed")
                        files_good = False
    if files_good:
        print("Files handled sucessfully")
    else:
        print("Error with overall files, please rerun program")

#add empty directory check
    # for folder in tmp
    for empty_folder in os.listdir(tmp_directory):
        # if is a directory and empty
        if os.path.isdir(empty_folder):
            os.rmdir(empty_folder)


# moves jpg -> .tmp folder (removing excess folders)
def move_jpg_tmp(file, path):
    try:
        shutil.move(file, path)
    except:
        print(f"File {file} not moved correctly")


def change_to_cbz(title):
    print("Making archive to convert to mobi")
    temp_dir = make_tempdir("")
    output_location = os.path.join(temp_dir ,title)
    try:
        shutil.make_archive(title, 'zip', temp_dir)
        cbz_path = temp_dir + title[:-4] + ".cbz" 
        os.rename()
    except:
        print("Error making zip file")


def get_title(zip_path): 
    names = sorted(os.listdir(zip_path))
    title_first_chapt = names[0].split(" ")[0]
    title_last_chapt = names[-1].strip().replace(' ', '').split("_")[1]
    title_last_chapt = f"_{title_last_chapt}"

    return title_first_chapt+title_last_chapt


def main():
    parser = argparse.ArgumentParser(description="Main file to merge files.")
    parser.add_argument('-o', '--output', help='output location', type=str, default=r'.\volumes')
    parser.add_argument('-p', '--path', help='path to your cbz archives', type=str, default=r'.\archives')
    args = parser.parse_args()

    title = get_title(args.path)

    # make volumes if doesn't already exist
     
    try:
        os.makedirs("volumes")
        print("made folder volumes")
    except FileExistsError:
        print("The folder volumes already exists, moving on")
    
    # extracts archives into .tmp
    extract(args.path) 
    print("Waiting for files to get into .tmp")
    time.sleep(1)
    print("Processing files...")
    # moves img files to .tmp and removes empty folders they came from
    handle_img_files()
    time.sleep(1)
    change_to_cbz(title)
    
    #os.rmdir(os.path.join(os.getcwd(),'.tmp'))

if __name__ == "__main__":
    main()

# todo:
    # make lists sort (more accurate)
