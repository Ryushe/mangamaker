from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
from utils.utils import non_specialify, is_similar


def search_retry_prompt(origional_anime):
  user_choice = input("Search failed. Retry (y/n/s(kip)) or enter new name: ").lower()
  if user_choice == 'n':
    sys.exit("exiting")
  elif user_choice == 's':
    return 'skip'
  elif user_choice == 'y':
    return origional_anime
  else:
    anime = user_choice
    return anime


class Site():
  def __init__(self, url, type=None, time=10):
    if type and type(type) != str: 
      self.driver = type
    elif type == "test":
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
    wait.until(EC.presence_of_element_located((method, id)))
  
  def wait_for_all(self, method, ids, time=10):
    wait = WebDriverWait(self.driver, time)
    wait.until(EC.presence_of_all_elements_located((method, ids)))
  
  def get_containers(self, id, method=By.CLASS_NAME):
    self.wait_for_all(method, self.container_element)
    containers = self.driver.find_elements(method, id)
    return containers
  
  def set_search_elements(self, 
                   search_bar_id, 
                   search_button_id,
                   manga_name_tag,
                   container_element=None, 
                   container_method=By.CLASS_NAME,
                   innercontainer_method=By.TAG_NAME):
    self.search_bar_id = search_bar_id
    self.search_button_id = search_button_id
    self.container_element = container_element
    self.manga_name_tag = manga_name_tag
    self.container_method = container_method
    self.innercontainer_method = innercontainer_method
  
  
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
    for container in self.manga_containers:
        self.container_name = container.find_element(self.innercontainer_method, self.manga_name_tag).text.lower() 
        if not self.filtered_name:
           self.filtered_name = non_specialify(self.container_name)
        if is_similar(self.search_query, self.filtered_name):
            print(f"{self.search_query} ==== {self.filtered_name}")
            a_tags = container.find_element(self.innercontainer_method, "a")
            self.url = a_tags.get_attribute("href")
            break
        self.url_found = True

  def search_for_manga_url(self, search_query, filter="default"):
    self.url_found = False
    potential_urls = []
    while not self.url_found:
        self.search_query = f"{search_query}"
        print(f"Searching for {search_query}")
        try:
            self.search_site()
            self.manga_containers = self.get_containers(self.container_element, self.container_method)
            self.set_filtered_name(filter) #filter_name in search_containers_for_url
            self.search_containers_for_url()

        except Exception as e:  
            self.search_query = search_retry_prompt(origional_anime=self.search_query)
            if self.search_query == 'skip':
                return None # dont think this exits anymore
    if self.url_found:
        print("Urls successfully found")
        print("boba"+self.url)
        return self.url

  def quit(self):
    self.driver.quit()
