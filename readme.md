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
5. `--kcc`
    - options found [here](https://github.com/ciromattia/kcc?tab=readme-ov-file#standalone-kcc-c2epy-usage) 
    - currently using `-u --croppingpower 0.80 --manga-style`
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
- The developer of KCC 
    - Found [here](https://github.com/ciromattia/kcc)