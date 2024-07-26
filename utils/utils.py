import itertools
import sys
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# not using
class Driver:
  def __init__(self):
    self.options = Options()
    self.options = webdriver.ChromeOptions() 
    self.options.add_argument("--log-level=3")
    self.options.add_argument('--headless')
    self.driver = webdriver.Chrome(options=self.options)
  def search(self, url):
    return self.driver.get(url)
  def wait(self, time):
    return WebDriverWait(self.driver, time)


def test_driver(url, time=10):
  driver = webdriver.Chrome()
  driver.get(url)
  wait = WebDriverWait(driver, time)
  return driver, wait
    
def make_driver(url, time=10):
  options = Options()
  options = webdriver.ChromeOptions() 
  options.add_argument("--log-level=3")
  options.add_argument('--headless')
  driver = webdriver.Chrome(options=options)
  driver.get(url)
  wait = WebDriverWait(driver, time)

  return driver, wait
  

def is_similar(str1, str2, max_diff=2):
  if abs(len(str1) - len(str2)) > max_diff:
    return False
  diff_count = 0
  for i in range(min(len(str1), len(str2))):
    if str1[i] != str2[i]:
      diff_count += 1
      if diff_count > max_diff:
        return False
  return True

def non_specialify(word):
  pattern = r"[^\w\s]"
  non_special_word = re.sub(pattern, '', word)
  return non_special_word.replace(',', '')


def dearray(nested_list):
  return list(itertools.chain.from_iterable(nested_list))

def is_decimal(number: str):
  if isinstance(number, str) and '.' in number:
    return True
  return False

def has_decimal(numbers):
  for num in numbers:
    if isinstance(num, float):
      return True
  return False  

def get_folder_files(path):
    folder_files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            folder_files.append(file_path)
    return folder_files
     


def cammel_case(words):
  split_words = words.split()
  capital = [word.capitalize() for word in split_words]
  capital_words = ' '.join(capital)
  return capital_words
  

class Site():
  def __init__(self, driver=None):
    if driver and type(driver) != str: 
      self.driver = driver
    elif driver == "test":
      self.driver = webdriver.Chrome()
    else:
      self.options = Options()
      self.options = webdriver.ChromeOptions() 
      self.options.add_argument("--log-level=3")
      self.options.add_argument('--headless')
      self.driver = webdriver.Chrome(options=self.options)
          
  def set_url(self, url):
      self.driver.get(url)
      print(self.driver.title)

  def button_search(self, searchbar_id, button_id, search_query, method=By.ID):
    search = self.driver.find_element(method, searchbar_id)
    search.clear()
    search.send_keys(search_query)
    button = self.driver.find_element(method, button_id)
    button.click()
  
  def wait_for(self, method, id, time=10):
    wait = WebDriverWait(self.driver, time)
    wait.until(EC.presence_of_element_located((method, id)))
  
  def wait_for_all(self, method, ids, time=10):
    wait = WebDriverWait(self.driver, time)
    wait.until(EC.presence_of_all_elements_located((method, ids)))
  
  def get_containers(self, id, method=By.CLASS_NAME):
    containers = self.driver.find_elements(method, id)
    return containers

  def quit(self):
    self.driver.quit()

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


