Used libs:
patoolib, shutil


# Instructions
1. `git clone https://github.com/Ryushe/mangamaker.git`
2. `pip install -r requirements.txt`, this will install all requirements needed 
3. move manga .zip files into the folder named archives
    - can find manga files [here](https://mangakatana.com/)
    - note: if archives folder isn't there, just make one in the project root directory
4. `python mangamaker.py [options]`

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
4. `--skip` (WIP)
    - skips to the very end and only uses kcc on files you want
	
# Todo
1. auto get downloaded zip files
2. find and download ico files for the anime