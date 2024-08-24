import subprocess
import patoolib
import os
import shutil
import time
import utils.get_covers as get_covers
import utils.tmp as tmp
import utils.get_amazon_metadata as get_amazon_metadata
import utils.metadata as metadata
import utils.download_katana_zips as download_katana_zips
from utils.utils import get_folder_files, cammel_case
import sys

def extract_files_to(files, directory): 
    # for file in archive(defualt) folder extract to .tmp
    for file in files:
        try:
            patoolib.extract_archive(file , outdir=directory)
        except: 
            print("these files already exist")


# renames and moves all .jpg files in tmp
def denest_imgs(img_dir):
    filename_count = 0
    files_good = True

    print("Processing files...")
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


def make_cbz_archive(title, img_dir, cbz_dir): 
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
    try:
        zip_path = os.path.join(input_folder)
        origional_names = sorted(os.listdir(zip_path))
        names = [os.path.splitext(name.replace(' ', ''))[0] for name in origional_names]
        folder_name = origional_names[0].split("_")[0]
        search_query = folder_name.replace('-', ' ')
        return names, folder_name, str(search_query).lower()
    except IndexError:
        print(f"{input_folder} is empty try again")
        sys.exit()


def get_titles(names, batch_size):
    lists = []
    for i in range(0, len(names), batch_size):
        lists.append(names[i:i+batch_size])

    titles = []
    for list in lists:
        print(list)
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

def remove_file(path):
    try:
        os.remove(path)
    except:
        print(f"Error removing {path}")


def move_to_folder(files, output, titles, tmp_folder=''): # not entirely sure works
    error = False
    remove_all = False
    if len(files) == len(titles):
        for file, title in zip(files, titles):
            try:
                final_path = os.path.join(output, title +'.mobi')
                if os.path.exists(final_path):
                    print(f"Found {final_path}")
                    if not remove_all:
                        user_choice = input("Would you like write over it? (y)es, (n)o, (a)ll: ").lower()
                        if user_choice == 'y':
                            remove_file(final_path)
                        elif user_choice == 'a':
                            remove_file(final_path)
                            remove_all = True
                        else:
                            continue
                    elif remove_all: 
                        remove_file(final_path)
                shutil.move(file, final_path)
            except shutil.Error as e:
                print(f"Error when moving file: {e}")
                error = True
            except OSError as e:
                print(f"Error deleting file: {e}")
                error = True
    else:
        print(f"length of files and item names arent the same somehow")
        print(f"you can find your files in .tmp/.tmp_covers ;-;")
    if not error:
        print(f"Successfully moved files into dir {output}")
    if tmp_folder:
        tmp_folder.close()


def start_points(args):
    option = str(args.use[0])
    if option == 'zips':
        print("What anime and how many:\nInput format: <anime> <start-end>")
        # usr_input = input("ex: berserk 50-200\n")
        # anime, *chapts = str(usr_input.replace("-",' ')).split(" ")
        # chapts = [int(chapt) for chapt in chapts]
        anime = "berserk"
        chapts = "1-100"
        download_katana_zips.main(anime, chapts, args.output)
        exit()

    # below items are for 
    archive_names, folder_name, search_query = get_names(args.input)
    titles = get_titles(archive_names, args.batch_size)
    if option == 'covers': 
        # get array of titles for filemetadata.py
        get_covers.main(anime=search_query, file_names=titles) 
    elif option == 'meta': #forces get of new covers
        allowing_get_path = tmp.TempDir()
        # if--> allowing for custom input for applying metadata
        if args.input != 'archives':
            if os.path.isdir(args.input):
                input_directory = args.input
            else:
                print(f"{args.input} is not a valid directory")
                sys.exit()
        else:
            input_directory = allowing_get_path.get_path('.tmp_kcc')
            allowing_get_path.close()
        files = get_folder_files(input_directory)
        output_folder = make_folder(args.output, folder_name)
        cover, covers_tmp = get_covers.main(anime=search_query, file_names=titles) 
        cover_files = sorted(get_folder_files(covers_tmp))

        book_data = get_amazon_metadata.main(search_query)
        if book_data: # assuming we have covers (since amazon the one thats messing up rn)
            metadata.apply(input_directory, covers_tmp, cammel_case(words=search_query), book_data)
        elif cover_files:
            metadata.apply(input_directory, covers_tmp, cammel_case(words=search_query))
        move_to_folder(files, output_folder, titles, cover) 
    else: 
        print(f"{option} not an option try again")


def run_full_program(args):
    # make volumes if doesn't already exist
    try:
        os.makedirs("volumes")
        print("made folder volumes")
    except FileExistsError:
        print("The folder volumes already exists, moving on")

    #thread 1    
    payload = args.kcc
    archive_paths = get_folder_files(args.input) 
    archive_names, folder_name, search_query = get_names(args.input)
    titles = get_titles(archive_names, args.batch_size)
    output_folder = make_folder(args.output, folder_name)
    title_index = 0


    img = tmp.TempDir()
    cbz = tmp.TempDir()
    kcc = tmp.TempDir()
    kcc_tmp = kcc.make_tempdir('.tmp_kcc')
    #covers_tmp -> same as above, use to close dir
    cover, covers_tmp = get_covers.main(anime=search_query, file_names=titles) 
    for i in range(0, len(archive_paths), args.batch_size):
        batch = archive_paths[i:i+args.batch_size]
        batch_names = archive_names[i:i+args.batch_size] 
        title = titles[title_index]
   
        # clears folder each time ;-;
        img_dir = img.make_tempdir('.tmp_img')
        cbz_dir = cbz.make_tempdir(".tmp_cbz")

        print(title)
        extract_files_to(batch, img_dir) 
        denest_imgs(img_dir) # moves img files to .tmp 
        make_cbz_archive(title, img_dir, cbz_dir) 
        print("Using KCC to crop and correct the images")
        #thread2 once 1 is done
        use_kcc(title, kcc_tmp, cbz_dir, payload) 
        title_index +=1

        img.close()
        cbz.close()
    #thread 
    book_data = get_amazon_metadata.main(search_query)
    metadata.apply(kcc_tmp, covers_tmp, cammel_case(words=search_query), book_data)

    kcc_paths = get_folder_files(kcc_tmp)
    move_to_folder(kcc_paths, output_folder, titles, kcc)

    # cover.close() 
    # kcc.close()
    

def main(args):

    # call different things based on args
    if args.use[0] != None:
        start_points(args)
        exit()
    else:
        run_full_program(args)
    

# todo:
    # make lists sort (more accurate)
    # check to see if can convert to cbz
    # add kcc in 
    # add error handling
