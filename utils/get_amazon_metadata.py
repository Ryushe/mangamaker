from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from utils.utils import *
import sys

def get_manga_url(anime):
    search_found = False
    potential_urls = []

    while not search_found:
        search_query = f"{anime}"
        print(f"Searching for {search_query}")
        try:
            amazon = Site()
            amazon.set_url("https://www.amazon.com/kindle-dbs/storefront?storeType=browse&node=154606011")
            amazon.wait_for(By.ID, "twotabsearchtextbox")
            amazon.button_search("twotabsearchtextbox", "nav-search-submit-button", search_query)
            amazon.wait_for_all(By.CLASS_NAME, "puisg-col-inner")
            amazon_containers = amazon.get_containers("puisg-col-inner")


            for container in amazon_containers:
                name = container.find_element(By.TAG_NAME, "span").text
                filtered_name = non_specialify(name.lower().split(' vol')[0])
                if is_similar(anime, filtered_name):
                    print(f"{anime} ==== {filtered_name}")
                    a_tags = container.find_element(By.TAG_NAME, "a")
                    link = a_tags.get_attribute("href")
                    break
            search_found = True

        except Exception as e:  
            anime = search_retry_prompt(anime)
            if anime == 'skip':
                return None
    
    if search_found:
        print("Urls successfully found")
    amazon.quit()
    try:
        return link
    except IndexError:
        print("Index error, exiting...")
        sys.exit()

def matches(text):
    options = ["asin", "publisher", "publication date"] # could add print length
    text = text.lower()
    for option in options:
        if option in text:
            return option

def metadata_time(url):
    driver, wait = make_driver(url)
    wait.until(EC.presence_of_element_located((By.ID, "detailBullets_feature_div")))
    author_text = driver.find_element(By.XPATH, "//span[@class='author notFaded']").text
    author = author_text.split(' ')[:-1]
    author_sort = f"{author[1]}, {author[0]}"
    author = f"{author[0]} {author[1]}"
    


    web_details = driver.find_elements(By.ID, "detailBullets_feature_div")
    
    book_details = {}
    for detail in web_details:
        spans = detail.find_elements(By.CLASS_NAME, "a-list-item")
        for span in spans:
            match = matches(span.text)
            if match:
                name, info = span.text.split(' : ')
                 
                book_details.update({name:info})
    book_details.update({"Author":author})
    book_details.update({"Author sort":author_sort})

    if book_details:
        print("Got book details")
        print(book_details)
    else: print("book details not found")
    return(book_details)



def main(anime):
    print("Getting amazon metadata")
    url = get_manga_url(anime)
    if url:
        book_details = metadata_time(url)
        return (book_details)
    else:
        return 

