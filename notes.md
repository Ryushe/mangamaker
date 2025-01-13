keeping a list of what I want to do:

`pipreqs .` -> gens req.txt

make linux and windows:
- check os and then use env variables
- run script that installs calibre x 7z (checks if installed) x adds to env variables so can pull into program
- docker container

urls that are used (mangakatana donwload hosters)
pixeldrain.com 
gofile.io

# Fixing:

# RN
- why no get url but thow error when return self.url
- search class bbg
    - need to fix search_container_for_url
        - make work with covers and amazon meta

# Known cooked logic
* mangamaker:
    * move files will say good move even if not at the end in (move_files)
- when then end name is chapter.5 it doesnt work (eg: 175.5)

# remember
- search loop doesnt exit properly anymore
- moved extract_numbrs to utils
- change cover by get_covers.py getindexes()

# Todo
- at this location `Search failed. Retry (y/n/s(kip))` make have a timeout
- covers not always being set correctly (maybe an index error?)
- upon initial run make create archives folder and then exit
- make output cuter and have a file dedicated to ascii art
- make --use azips (this will auto download, if not has an option box to download the item)
- when using issimilar, i could compare all results and see which is the closest
- think while loop in get_covers is useless
- make cli args more intuitive (eg: --zips --covers)
    - this way you don't have to say --use ... and if i want covers and zips I can
- make searches option to retry, new query or a time out skip (no input will skip)
- could add to metadata.py duplicate covers based on number value
    - eg: chapt 50 would duplicate the cover associated with 50
- migrate the get_covers and amazon -> the site class (see download_katana_zips.py)
- if cover not found use the one from mangakatana

- download zips:
    - make the name more intuitive (have multiple options instead of use <option>)

- amazon meta.py:
    - only apply the data it was able to retrieve(IMPORTANT)
    - have data based on volumes
    - get book data if fails
    - add skip functionality

- get_covers:
    - change when it gets the covers, eg: if I give 1-200 make when it splits it thats when it uses the cover to apply
    - if fails make option to repeat
    - make compare name in potential urls list, one closest gets added

- general:
    - make auto impaort from downloads
    - threads lol
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
    - make zips option cleaner (right now shitty input system)

- web_search:
    - for i, num in enumerate (getting 2nd index) kinda poor, would be good to find max


# done
* cover length different from actual files for some reason 
    - `length of files and item names arent the same somehow`
- include all info about the file in metadata
    - get_amazon_meta -> add items to dict from the spans
        - really all need to do is add to options array
    - apply_metadata -> update calibre command
- move between kcc_tmp and output
- method to clear temp dirs -> (allowing for resume)
- fixing meta
    - going to need to change run all as well

# Bugs 
- Currenly fixing
    - null

- fixed
    - get_amazon_metadata search not working ;-;
    - sorted(get_folder_files(kcc_tmp)) -----> bug

- known bugs
    - if kcc output ends up being too big (it auto splits it)
        - meaning in mangamaker move_file len==len doesnt work
            - duplicate cover or something ;-;
        - also when applying cover in metadata is bad to
    - command for metadata not appling everything (series)
        - has 'name for some reason
    - get_covers sometimes errors out with no covers...
        - possible fix higher wait time or if fail retry
    - not working on linux
    - getting covers not always accurate

 
  

{'ASIN': 'B073ZJV2VG', 'Publisher': 'Dark Horse Manga; 1st Edition (July 18, 2017)', 'Publication date': 'July 18, 2017', 'Print length': '224 pages', 'Author': 'Kentaro Miura', 'Author sort': 'Miura, Kentaro'}

ebook-meta "D:\Code\Python\mangamaker\volumes\gantz_test.mobi" -a test --isbn amazon:booba --cover "D:\Code\Python\mangamaker\.tmp\.tmp_covers\king-game_c001+_+c050.jpg"
