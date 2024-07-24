import itertools
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

  return [file for file in os.listdir(path) 
          if os.path.isfile(os.path.join(path, file))]

