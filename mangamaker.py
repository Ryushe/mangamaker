import subprocess
import patoolib
import os
import shutil
import time
import utils.get_covers as get_covers
import utils.tmp as tmp

def extract(batch, img_dir): 
    # for file in archive(defualt) folder extract to .tmp
    for file in batch:
        try:
            patoolib.extract_archive(file , outdir=img_dir)
        except: 
            print("these files already exist")


# renames and moves all .jpg files in tmp
def handle_img_files(img_dir):
    filename_count = 0
    files_good = True

    # for folder in .tmp do..
    for folder in os.listdir(img_dir):
        folder_path = os.path.join(img_dir, folder)
        # check if is folder in .tmp
        if os.path.isdir(folder_path):
            # for file in the folder
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                # print(f"Working on file:\n{file_path}")
                if os.path.isfile(file_path) and file_path.endswith(".jpg"):
# add other img functionality
                    try:
                        new_filename = f"{filename_count}.jpg"
                        new_filepath = os.path.join(img_dir, f"{filename_count}.jpg") # .tmp + new_filename

                        new_filename = os.path.join(folder_path, new_filename)
                        # print(f"Renaming: {file}")
                        os.rename(file_path, new_filename)
                        filename_count += 1

                        # moves jpg files in folders -> tmp
                        move_jpg_tmp(new_filename, new_filepath)
                    
# could add a rerun feature if failed
                    except:
                        print(f"file {file} could't be renamed")
                        files_good = False
    if files_good:
        print("Files handled sucessfully")
        # deltes empty folders
        for folder in os.listdir(img_dir):
            folder_path = os.path.join(img_dir, folder)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
    else:
        print("Error with overall files, please rerun program")
        exit()

#add empty directory check
    # for folder in tmp
    for empty_folder in os.listdir(img_dir):
        # if is a directory and empty
        if os.path.isdir(empty_folder):
            os.rmdir(empty_folder)


# moves jpg -> .tmp folder (removing excess folders)
def move_jpg_tmp(file, path):
    try:
        shutil.move(file, path)
    except:
        print(f"File {file} not moved correctly")


def change_to_cbz(title, img_dir, cbz_dir): 
    print("Making archive to convert to mobi")
    try:
        zip_path = os.path.join(cbz_dir, title)
        shutil.make_archive(zip_path, 'zip', img_dir) # output, type, source
        cbz_path = os.path.join(cbz_dir, title + ".cbz")
        os.rename(zip_path + ".zip", cbz_path) 
        time.sleep(1)
        print("Sucessfully made a .cbz file")
    except FileExistsError:
        print(f"{title}.cbz already exists")
    except:
        print("Error making .cbz file")


def use_kcc(title, output, cbz_dir, payload):
    # output = os.path.join(os.getcwd(),output)
    output = os.path.abspath(output)
    print('output = '+output)
    input = os.path.join(cbz_dir,title+'.cbz')
    print('input = '+input)
    command = f'python manga_format_maker\\kcc-c2e.py {payload} -o {output} {input}'

    subprocess.run(command, shell=True)

def get_names(input_folder):
    zip_path = os.path.join(input_folder)
    origional_names = sorted(os.listdir(zip_path))
    names = [name.replace(' ', '')[:-4] for name in origional_names]
    folder_name = origional_names[0].split("_")[0]
    search_query = origional_names[0].split("_")[0].replace("-", " ")
    return names, folder_name, str(search_query)


def get_titles(names, batch_size):
    lists = []
    for i in range(0, len(names), batch_size):
        lists.append(names[i:i+batch_size])

    titles = []
    for list in lists:
        name = list[0].split("_")[0]
        first = list[0].split("_")[1]
        last = list[-1].split("_")[2]
        titles.append( f"{name}_{first}_{last}")
        
    return titles

def make_folder(path, name):
    try:
        path = os.path.join(path, name)
        os.mkdir(path)
    except FileExistsError:
        print(f"{name} already exists")
    return path

def good_ol_metadata():
    path = os.path.join(os.getcwd(), "utils", "metadata.py")
    command = f"calibre-debug {path}"
    subprocess.run(command, shell=True, check=True)


def main(args):
    payload = args.kcc
    archive_paths = [os.path.join(args.input, f) for f in os.listdir(args.input) if os.path.isfile(os.path.join(args.input, f))]
    archive_names, folder_name, search_query = get_names(args.input)
    titles = get_titles(archive_names, args.batch_size)
    kcc_output_folder = make_folder(args.output, folder_name)
    title_index = 0
    if args.imgs: 
        # get array of titles for filemetadata.py
        get_covers.main(anime=search_query.lower(), file_names=titles) 
        exit()

    # make volumes if doesn't already exist
    try:
        os.makedirs("volumes")
        print("made folder volumes")
    except FileExistsError:
        print("The folder volumes already exists, moving on")

    img = tmp.TempDir()
    cbz = tmp.TempDir()
    cover_paths, covers_tmp = get_covers.main(anime=search_query.lower(), file_names=titles) 
    for i in range(0, len(archive_paths), args.batch_size):
        batch = archive_paths[i:i+args.batch_size]
        batch_names = archive_names[i:i+args.batch_size] 
        title = titles[title_index]
   
        img_dir = img.make_tempdir('.tmp_img')
        cbz_dir = cbz.make_tempdir(".tmp_cbz")

        print(title)
        print(batch, batch_names)
        extract(batch, img_dir) # for file in input dir -> extracts to img_dir
        print("Processing files...")
        # moves img files to .tmp and removes empty folders they came from
        handle_img_files(img_dir)
        change_to_cbz(title, img_dir, cbz_dir) 
        print("Using KCC to crop and correct the images")
        use_kcc(title, kcc_output_folder, cbz_dir, payload) 
        title_index +=1

        img.close()
        cbz.close()

# todo:
    # make lists sort (more accurate)
    # check to see if can convert to cbz
    # add kcc in 
    # add error handling
