# from utils.utils import
from utils.web_search import Site
from selenium.webdriver.common.by import By


def main(search_query, output_dir):
    manga_katana = Site("https://mangakatana.com/", "test")
    manga_katana.set_search_elements("input_search",
                                      "searchsubmit", 
                                      "title", By.CLASS_NAME,
                                      "a", By.TAG_NAME)
    url = manga_katana.search_for_manga_url(search_query)
    print(url)


