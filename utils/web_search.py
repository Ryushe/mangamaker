from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
from utils.utils import *


def search_retry_prompt(origional_anime):
  user_choice = input("Retry? (y/n/s(kip)) or enter new name: ").lower()
  if user_choice == 'n':
    sys.exit("exiting")
  elif user_choice == 's':
    return 'skip'
  elif user_choice == 'y':
    return origional_anime
  else:
    anime = user_choice
    return anime


# defferent than make_driver() because this has to do with the class handling, once change get meta/cover can only use this
def make_new_driver( url=None, type_=None, time=12):
  if type_ and type(type_) != str: 
    driver = type_
  elif type_ == "test":
    driver = webdriver.Chrome()
  else:
    options = Options()
    options = webdriver.ChromeOptions() 
    options.add_argument("--log-level=3")
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
  wait = WebDriverWait(driver, time) 
  if url:
    driver.get(url)
    print(driver.title)


class Site():
  # could replace for make_new_driver
  def __init__(self, url, type_=None, time=12):
    if type_ and type(type_) != str: 
      self.driver = type_
    elif type_ == "test":
      self.driver = webdriver.Chrome()
    else:
      self.options = Options()
      self.options = webdriver.ChromeOptions() 
      self.options.add_argument("--log-level=3")
      self.options.add_argument('--headless')
      self.driver = webdriver.Chrome(options=self.options)
    self.wait = WebDriverWait(self.driver, time) 
    self.driver.get(url)
    print(self.driver.title)
  
  def set_url(self, url):
      self.driver.get(url)
      print(self.driver.title)

  def button_search(self, searchbar_id, button_id, search_query, method=By.ID):
    self.search = self.driver.find_element(method, searchbar_id)
    self.search.clear()
    self.search.send_keys(search_query)
    self.button = self.driver.find_element(method, button_id)
    self.button.click()
  
  def wait_for(self, method, id, time=10):
    wait = WebDriverWait(self.driver, time)
    self.wait.until(EC.presence_of_element_located((method, id)))
  
  def wait_for_all(self, method, ids, time=10):
    wait = WebDriverWait(self.driver, time)
    self.wait.until(EC.presence_of_all_elements_located((method, ids)))
  
  def get_containers(self, class_name, method=By.CLASS_NAME):
    self.wait_for_all(method, self.container_element)
    containers = self.driver.find_elements(method, class_name)
    return containers
  
  def set_search_elements(self, 
                   search_bar_id, 
                   search_button_id,
                   container_element, container_method,
                   manga_name_tag, manga_method=By.TAG_NAME):
    self.search_bar_id = search_bar_id
    self.search_button_id = search_button_id
    self.container_element = container_element
    self.container_method = container_method
    self.manga_name_tag = manga_name_tag
    self.manga_method = manga_method
  
  
  def search_site(self, search_bar_element='', search_button_element='', search_query=''):
    # if given proper args, search site for the query
    if search_bar_element and search_button_element and search_query:
        self.wait_for(By.ID, search_bar_element)
        self.button_search(search_bar_element, search_button_element, search_query)
    else:
        self.wait_for(By.ID, self.search_bar_id)
        self.button_search(self.search_bar_id, self.search_button_id, self.search_query)
    
  def search_amazon_containers_url(self):
      # since going to need to be special
    return
  
  def set_filtered_name(self, filter):
    if filter == "amazon":
      # can totally make better 
      self.filtered_name = non_specialify(self.container_name.lower().split(' vol')[0])
    else:
      self.filtered_name = non_specialify(self.container_name)

    # continue 
  def search_containers_for_url(self):
    print(self.manga_containers)
    for container in self.manga_containers:
        self.container_name = container.find_element(self.manga_method, self.manga_name_tag).text.lower() 
        self.set_filtered_name(self.filter_) #filter_name in search_containers_for_url
        if is_similar(self.search_query, self.filtered_name):
            print(f"{self.search_query} ==== {self.filtered_name}")
            a_tags = container.find_element(self.manga_method, "a")
            self.url = a_tags.get_attribute("href")
            break
        self.url_found = True

  def search_for_manga_url(self, search_query, filter_="default"):
    self.url_found = False
    self.filter_ = filter_
    potential_urls = []
    while not self.url_found:
        self.search_query = f"{search_query}"
        print(f"Searching for {search_query}")
        try:
            self.search_site()
            self.manga_containers = self.get_containers(self.container_element, self.container_method)
            self.search_containers_for_url()

        except Exception as e:  
          print(f"error {e}")
          self.search_query = search_retry_prompt(origional_anime=self.search_query)
          if self.search_query == 'skip':
              return None # dont think this exits anymore
    if self.url_found:
        print("Urls successfully found")
        return self.url
  

  def get_chapter_urls(self, chapters_container, input_chapters):
    max_chapt_nums = []
    chapt_urls = []
    # gets max chapt nums from b tags
    for chapter in chapters_container:
      chapter_tags = chapter.find_elements(By.TAG_NAME, "b")
      chapter_nums = [chapter.text for chapter in chapter_tags]
      urls = chapter.find_elements
      for i, num in enumerate(chapter_nums):
        if i % 2 == 1: # bad logic
          max_chapt_nums.extend(extract_numbers(num))
          chapt_urls.append(chapter.find_element(By.TAG_NAME, "a").get_attribute("href"))

    # checking if in range, if so will add the url to the list
    for num, url in zip(max_chapt_nums, chapt_urls):
      if num in range(input_chapters[0], input_chapters[1]+1):
        print(f"{num} found in range {input_chapters[0]}-{input_chapters[1]}")       
        print(f"chapt {num}: {url}")
  
  def bot_handler(self):
    return
  # continue (need capache bypass/wait for user to complete capache)

  def download_archives(self, input_chapters, output, url=None):
    urls = []
    if url is None:
      url = self.url+"/download"
    self.driver.get(url)
    print("download url: "+url)
    self.wait_for_all(By.CLASS_NAME, "chapter")
    chapters_container = self.get_containers("chapter")
    input_chapters = [2, 40]
    max_chapter_nums = self.get_chapter_urls(chapters_container, input_chapters)


  def quit(self):
    self.driver.quit()
