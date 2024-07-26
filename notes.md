keeping a list of what I want to do:

`pipreqs .` -> gens req.txt

# RN
- fixing meta
    - going to need to change run all as well
  
# if go back
- final_path = os.path.join(output, title, '.mobi') 
    - change , to a +
- def get_folder_files(path):
    folder_files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            folder_files.append(file_path)
    return folder_files
- remove get_paths in metadata

# Todo
- amazon meta.py:
    - have data based on volumes
    - get book data if fails
    - add skip functionality

- get_covers:
    - if fails make option to repeat
    - make compare name in potential urls list, one closest gets added

- general:
    - clean up start points meta (a mess)
    - when spilt name with .vol if it doesnt find .vol use something else, eg: a number (regex)
    -  parser.add_argument('--use', help='use: set(meta), dowload(covers)', type=str, nargs=1)
        - make this havem more args (optional)
        - input/output args
    - make metadata get all metadata instead of get_amazon_metadat
    - break the main clutter in (run_full_program) into little ones
        - making calling sub easier
    - resume anywhere 
    - make tmp dir, if finds files of the same type working on resumes instead of removing them
    - take input from downloads and archives
    - have volumes chapts closer to how they work (allowing for more accurate progress)
    - could have close() close all tmp
        - since tmp can make multiple tmps under the same instance

- mangamaker:
    - make meta option use new covers/or old covers

# done
- include all info about the file in metadata
    - get_amazon_meta -> add items to dict from the spans
        - really all need to do is add to options array
    - apply_metadata -> update calibre command
- move between kcc_tmp and output
- method to clear temp dirs -> (allowing for resume)

# Bugs 

- Currenly fixing
    - null

- fixed
    - get_amazon_metadata search not working ;-;
    - sorted(get_folder_files(kcc_tmp)) -----> bug

- known bugs
    - command for metadata not appling everything (series)
        - has 'name for some reason
    - get_covers sometimes errors out with no covers...
        - possible fix higher wait time or if fail retry

 
  

{'ASIN': 'B073ZJV2VG', 'Publisher': 'Dark Horse Manga; 1st Edition (July 18, 2017)', 'Publication date': 'July 18, 2017', 'Print length': '224 pages', 'Author': 'Kentaro Miura', 'Author sort': 'Miura, Kentaro'}

ebook-meta "D:\Code\Python\mangamaker\volumes\gantz_test.mobi" -a test --isbn amazon:booba --cover "D:\Code\Python\mangamaker\.tmp\.tmp_covers\king-game_c001+_+c050.jpg"
