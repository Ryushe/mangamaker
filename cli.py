import argparse
import mangamaker as mangamaker

def cli():
    parser = argparse.ArgumentParser(description="Main file to merge files.")
    parser.add_argument('-o', '--output', help='output location (full path)', type=str, default=r'volumes') # might be broken (have to specify path in weird ways)
    parser.add_argument('-i', '--input', help='path to your cbz archives', type=str, default=r'archives')
    parser.add_argument('--keep', help='Keep cbz files default:false (True/False)', type=bool, default=False)
    parser.add_argument('--batch_size', help='How many zip files to put in each mobi (5)', type=int, default=5)
    parser.add_argument('--imgs', help='only get cover images',action='store_true') 
    parser.add_argument('--skip', help='only use kcc with local archives folder', type=bool, default=False) 
    args = parser.parse_args()

    mangamaker.main(args)

cli()

# add functionality (make it so that if you already have the cbz you can just use kcc on it)

      