# from utils.utils import
from utils.web_search import Site
from selenium.webdriver.common.by import By
from utils.utils import *
import time

# NOT COMPLETED 
# don't think this will be integrated into the full app. but rather an option in the app

# will check to see if read offline is present (means on the correct section of the page)
# allows for handling if only one anime that name

def handle_selection(urls, names):
    count = 0
    print(f"""
Enter the number for the anime

options: 
  - valid number
  - exit/e
""")
    for url,name in zip(urls, names):
        print(f"  [{count}]: {name}")
        print(f"  url: {url}")
        count+=1
    while True:
        try: 
            index = int(input("\nNumber: "))
            if index == "exit" or index == "e":
                print("Exiting...")
                sys.exit()
            return urls[index], names[index]
        except ValueError:
            print("Your input wasn't an integer, try again")
        except IndexError:
            print("Your input was not in range try again")


def main(anime, chapts, output_dir, auto=False):
    print("""
#################################
#                               #
#      D O W N L O A D E R      #
#                               #
#################################
""")
    mangakatana = Site("test")
    mangakatana.set_url(f"https://mangakatana.com/?search={anime}&search_by=book_name")
    mangakatana.wait_for_all(By.CLASS_NAME, "item")
    manga_container = mangakatana.get_containers("item")
    anime_url = mangakatana.current_url
    if manga_container:
        if auto:
            anime_url = mangakatana.search_container_for_url(manga_container, anime)
        else:
            names, urls = mangakatana.search_container_for_urls(manga_container)
            anime_url, anime_name = handle_selection(urls, names)
    mangakatana.set_url(anime_url+"/download")

    ## currently getting anime url auto and not (and at the download portion)
    ## todo:
    ## - make dowlnload the archives
    ## - bypass ai check (human intervention for now)

    # assuming only one search for item -- if no hit on if
    # mangakatana.get_containers()
    # read_page(mangakatana)
