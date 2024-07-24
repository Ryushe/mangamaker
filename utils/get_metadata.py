from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from get_covers import make_driver
from fns import *

def main():
    potential_urls = []
    driver, wait = make_driver("https://www.amazon.com/books-used-books-textbooks/b?ie=UTF8&node=283155")
    
    while not search_found:
      try:
          wait.until(EC.presence_of_element_located((By.ID, "header-search-input")))
          title = driver.title
          print(title)

          search = driver.find_element(By.ID, "header-search-input")
          search.send_keys(anime)

          wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "dense-manga-container")))

          manga_containers = driver.find_elements(By.CLASS_NAME, "dense-manga-container")
          for manga in manga_containers:
              web_manga_name = manga.find_element(By.TAG_NAME, "div").text.lower()
              no_special_char = non_specialify(web_manga_name)
              if(is_similar(anime, no_special_char)):
                  potential_urls.append(manga.find_element(By.TAG_NAME, "a").get_attribute("href"))
          search_found = True

      except Exception as e:  
          user_choice = input("Search failed. Retry (y/n) or enter new name: ").lower()
          if user_choice == 'n':
              break 
          else:
              anime = user_choice
              search.clear()
    print("Urls successfully found")
    driver.quit()
    try:
        return potential_urls[0]
    except IndexError:
        print("Cant find that anime")
        print("Relaunch using the flag --imgs")
        exit()
