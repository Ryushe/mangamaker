keeping a list of what I want to do:

`pipreqs .` -> gens req.txt

# RN
- making run all into small fns

# Todo
- amazon meta.py:
    - have data based on volumes
    - get book data if fails

- get_covers:
    - make compare name in potential urls list, one closest gets added

- general:
    -  parser.add_argument('--use', help='use: set(meta), dowload(covers)', type=str, nargs=1)
        - make this havem more args (optional)
        - input/output args
    - break the main clutter in (run_full_program) into little ones
        - making calling sub easier
    - resume anywhere 
    - make tmp dir, if finds files of the same type working on resumes instead of removing them
    - take input from downloads and archives
    - have volumes chapts closer to how they work (allowing for more accurate progress)
    - could have close() close all tmp
        - since tmp can make multiple tmps under the same instance

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
