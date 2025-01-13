# Manga Maker
![manga](./manga.jpeg)
External dependencies not in req.txt: Calibre
Used in proj:  
patoolib, shutil, KCC, patool, PySide6, Pillow, psutil, requests, python-slugify, raven, mozjpeg-lossless-optimization, natsort, distro, selenium

## Windows
1. `git clone https://github.com/Ryushe/mangamaker.git`
2. `pip install -r requirements.txt`, this will install all requirements needed 
    - instructions for virtual environment found below
3. install calibre found [here](https://calibre-ebook.com/download)
4. install kindle-previewer found [here](https://www.amazon.com/Kindle-Previewer/b?ie=UTF8&node=21381691011)
  
5. put manga .zip files into input folder (default: archives)
    - can find manga files [here](https://mangakatana.com/)
    - note: if archives folder isn't there, just make one in the project root directory
6. `python cli.py [options]` or `run.bat`

Note: If you have a diferent kindle you may want to customize the kcc payload  
- `--kcc <kcc options>`
- options found [here](https://github.com/ciromattia/kcc?tab=readme-ov-file#standalone-kcc-c2epy-usage)
- current payload `-u --croppingpower 0.80 --manga-style`

## Linux Install
1. `git clone https://github.com/Ryushe/mangamaker.git`
2. `pip install -r requirements.txt`, this will install all requirements needed 
3. install calibre [here](https://calibre-ebook.com/download)
    - or install command: `sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin`
4. install 7z: 
    - ubuntu `sudo apt install p7zip-full`
    - arch `sudo pacman -S p7zip`
5. install kinglegen:
    - `curl https://archive.org/download/kindlegen_linux_2_6_i386_v2_9/kindlegen_linux_2.6_i386_v2_9.tar.gz -o kindlegen.tar.gz`
    - `tar -xzvf kindlegen.tar.gz -C kindlegen`
    - `sudo mv kindlegen/kindlegen /usr/local/bin`
      - makes file executable anywhere
    - `rm -rf kindlegen`
6. put manga .zip files into input folder (default: archives)
    - can find manga files [here](https://mangakatana.com/)
    - note: if archives folder isn't there, just make one in the project root directory
7. `python cli.py [options]` or `run.bat`

## Venv
A virtual environment allows you to not have to worry about managing versions of libraries. It sets this python environment for this project specifically.

Creating one:
1. `pip install virtualenv`
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `which python` - should list your current directory

## Docker
1. `docker build -t mangamaker .`

## Usage
Current options:
1. `-o, --output`
    - output location of the .mobi file
    - default: volumes
2. `-i, --input`
    - path to your cbz archives/.mobi files for editing meta data
    - default: archives
3. `--keep`
    - doesn't remove the img/cbz folders when finished
    - default: False (doesn't keep them)
4. `--batch_size`
    - How many zip files to put in each mobi
    - default: 5
5. `--use`
    - options:
        - meta (default volume collection input: /tmp/.tmp_kcc)
            - gets amazon metadata (author, asin, etc)
            - gets volume covers (gets new volume cover after 50 chaps)
            - note: custom input not yet supported
        - covers 
            - dowloads covers for volumes
            - gets new volume cover every 50 chapters

Notes: 
- if using own manga zip files make sure their names end with `_cnumber_cnumber`  
- ex: `chainsawman_c101_c150`, `one-piece_c150_c160`


## How I use this tool
Currently I have a paper edition kindle 
- install zip files from [MangaKatana](https://mangakatana.com/). This site lets you download manga in zip files
- drag zip files into the input dir (default: archives)
- click on run.bat
- ggs, now you have the volume covers and the manga to go with it
    - note: covers found in `.tmp/.tmpcovers`

## FAQ
Q: When the program extracts the files I get a "can't rename image"
A: Open up the directory of the program and go to `.tmp/.tmp_img` you should see a folder that still contains data. This is the problem folder. Take all of the files contents, put it in a new folder and then put that new folder into the archive (replacing the old).

## Todo
1. auto get downloaded zip files
2. find and download ico files for the anime


## Shoutouts
Big thanks to:
- Developer of KCC 
    - Found [here](https://github.com/ciromattia/kcc)
- Kovid Goyal (Calibre ebook-meta)

python version 3.12.6