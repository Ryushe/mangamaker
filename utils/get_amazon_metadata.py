from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from utils.utils import *

def get_manga_url(anime):
    potential_urls = []
    driver, wait = make_driver("https://www.amazon.com/kindle-dbs/storefront?storeType=browse&node=154606011")
    search_found = False

    while not search_found:
        search_query = f"{anime} vol manga"
        try:
            wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            title = driver.title
            print(title)

            search = driver.find_element(By.ID, "twotabsearchtextbox")
            search.clear()
            search.send_keys(search_query)
            search_button = driver.find_element(By.ID, "nav-search-submit-button")
            search_button.click()

            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "puisg-col-inner")))
            amazon_containers = driver.find_elements(By.CLASS_NAME, "puisg-col-inner")

            for container in amazon_containers:
                name = container.find_element(By.TAG_NAME, "span").text
                filtered_name = name.split(',')[0].lower()
                if is_similar(anime, filtered_name):
                    print(f"{anime} ==== {filtered_name}")
                    a_tags = container.find_element(By.TAG_NAME, "a")
                    link = a_tags.get_attribute("href")
                    break
            search_found = True

        except Exception as e:  
            user_choice = input("Search failed. Retry (y/n) or enter new name: ").lower()
            if user_choice == 'n':
                break 
            else:
                anime = user_choice
    print("Urls successfully found")
    driver.quit()
    try:
        return link
    except IndexError:
        print("Cant find that anime")
        print("Relaunch using the flag --imgs")
        exit()

def matches(text):
    options = ["asin", "publisher", "publication date", "print length"]
    text = text.lower()
    for option in options:
        if option in text:
            return option

def metadata_time(url):
    driver, wait = test_driver(url)
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

    return(book_details)



def main(anime):
    url = get_manga_url(anime)
    book_details = metadata_time(url)
    return (book_details)

