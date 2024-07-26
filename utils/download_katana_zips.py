# from utils.utils import
from utils.web_search import Site
from selenium.webdriver.common.by import By

def main(search_query):
    manga_katana = Site("https://mangakatana.com/")
    manga_katana.set_search_elements("input_search", "searchsubmit", "a", "book_list", By.ID)
    url = manga_katana.search_for_manga_url(search_query)
    print(url)


