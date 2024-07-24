keeping a list of what I want to do:

`pipreqs .` -> gens req.txt

amazon meta.py:
- have data based on volumes
- get book data if fails

get_covers:
- make compare name in potential urls list, one closest gets added

general:
- resume anywhere 
- make tmp dir, if finds files of the same type working on resumes instead of removing them
- take input from downloads and archives
- have volumes chapts closer to how they work (allowing for more accurate progress)
- include all info about the file in metadata
    - get_amazon_meta -> add items to dict from the spans
        - really all need to do is add to options array
    - apply_metadata -> update calibre command
- could have close() close all tmp
    - since tmp can make multiple tmps under the same instance

adding:
- move between kcc_tmp and output
- method to clear temp dirs -> (allowing for resume)

Currenly fixing:
- null

fixed:
- get_amazon_metadata search not working ;-;
- sorted(get_folder_files(kcc_tmp)) -----> bug

known bugs:
- get_covers sometimes errors out with no covers...
    - possible fix higher wait time or if fail retry

 
  

{'ASIN': 'B073ZJV2VG', 'Publisher': 'Dark Horse Manga; 1st Edition (July 18, 2017)', 'Publication date': 'July 18, 2017', 'Print length': '224 pages', 'Author': 'Kentaro Miura', 'Author sort': 'Miura, Kentaro'}

ebook-meta "D:\Code\Python\mangamaker\volumes\gantz_test.mobi" -a test --isbn amazon:booba --cover "D:\Code\Python\mangamaker\.tmp\.tmp_covers\king-game_c001+_+c050.jpg"



when get --kcc done


Used in proj:  
patoolib, shutil, KCC, patool, PySide6, Pillow, psutil, requests, python-slugify, raven, mozjpeg-lossless-optimization, natsort, distro, selenium

# Instructions
1. `git clone https://github.com/Ryushe/mangamaker.git`
2. `pip install -r requirements.txt`, this will install all requirements needed 
3. move manga .zip files into input folder (default: archives)
    - can find manga files [here](https://mangakatana.com/)
    - note: if archives folder isn't there, just make one in the project root directory
4. `python mangamaker.py [options]` or `run.bat`

Note: If you have a diferent version you may want to customize the kcc payload  
- `--kcc <kcc options>`
- options found [here](https://github.com/ciromattia/kcc?tab=readme-ov-file#standalone-kcc-c2epy-usage)
- current payload `-u --croppingpower 0.80 --manga-style`

# Usage
Current options:
1. `-o, --output`
    - output location of the .mobi file
    - default: volumes
2. `-i, --input`
    - path to your cbz archives
    - default: archives
3. `--keep`
    - doesn't remove the img/cbz folders when finished
    - default: False (doesn't keep them)
4. `--batch_size`
    - How many zip files to put in each mobi
    - default: 5
6. `--skip` (WIP)
    - skips to the very end and only uses kcc on files you want

Notes: 
- if using own manga zip files make sure their names end with `_cnumber_cnumber`  
- ex: `chainsawman_c101_c150`, `one-piece_c150_c160`


# How I use this tool
Currently I have a paper edition kindle 
- install zip files from [MangaKatana](https://mangakatana.com/). This site lets you download manga in zip files
- drag zip files into the input dir (default: archives)
- click on run.bat
- ggs, now you have the volume covers and the manga to go with it
    - note: covers found in `.tmp/.tmpcovers`

	
# Todo
1. auto get downloaded zip files
2. find and download ico files for the anime


# Shoutouts
Big thanks to:
- Developer of KCC 
    - Found [here](https://github.com/ciromattia/kcc)
- Kovid Goyal (Calibre ebook-meta)
