# from utils.utils import
from utils.web_search import Site
from selenium.webdriver.common.by import By

# NOT COMPLETED 

def main(search_query, chapts, output_dir):
    manga_katana = Site("https://mangakatana.com/", "test")
    manga_katana.set_search_elements("input_search",
                                      "searchsubmit", 
                                      "title", By.CLASS_NAME,
                                      "a", By.TAG_NAME)
    url = manga_katana.search_for_manga_url(search_query)
    manga = manga_katana.download_archives(chapts, output_dir)
    # manga = MangaDownloader()


