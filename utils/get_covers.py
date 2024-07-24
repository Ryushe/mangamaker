# this file will handle the metadata of the file, eg: get the manga pics, apply those pics to the cbz file, add the amazin ibn number, author, etc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import utils.tmp as tmp
import re
import os
from utils.utils import *

def get_manga_url(anime): 
  driver, wait = make_driver("https://mangadex.org/")
  search_found = False
  potential_urls = []

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
                print(anime, no_special_char)
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



def get_img_urls(url):
  driver, wait = make_driver(url+"?tab=art")
  wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "subtitle")))
  cover_urls = driver.find_elements(By.CSS_SELECTOR, "img[data-v-2763eefc]")[1:]
  volume_names = driver.find_elements(By.CSS_SELECTOR, "span[data-v-2763eefc]")
  volume_nums = dearray([extract_numbers(num.text) for num in volume_names]) # hehe

  new_cover_urls = []
  for i in range(0,len(volume_nums)): 
    if has_decimal(volume_nums):
      try:
        if is_decimal(str(volume_nums[i])):
          new_cover_urls.append(cover_urls[i].get_attribute("src"))
      except:
        print("fuck uself")
    else: 
      new_cover_urls.append(cover_urls[i].get_attribute("src"))
  driver.quit()
  return new_cover_urls


def extract_numbers(string): # takes 1 arg no list
  decimal = False
  numbers = re.findall(r'-?\d+\.?\d*', string)
  for num in numbers:
    if is_decimal(num):
      decimal = True
  if decimal:
    return [float(num) for num in numbers]
  else:
    return [int(num) for num in numbers]
  

def get_indexes(file_names):
  extracted_int = extract_numbers(file_names[0])
  chapters_per = max(extracted_int) - (min(extracted_int) - 1)
  start_index = max(1, min(extracted_int) // 50) # if want to make by chapts change to chapters_per
  end_index = start_index + len(file_names)
  
  return start_index, end_index


# makes cover_urls and filenames even in length and returns items based on the volume numbers in the file names
def correctly_indexed_cover_urls(file_names, cover_urls):
  new_urls = []
  if len(cover_urls) > len(file_names): 
    start, end = get_indexes(file_names)
    return cover_urls[start:end] 
  elif len(cover_urls) < len(file_names): 
    new_urls = cover_urls[:]
    while len(new_urls) != len(file_names):
      new_urls.append(cover_urls[-1])
    return new_urls
  elif len(cover_urls) == len(file_names):
    return cover_urls

 
def download_covers(cover_urls, file_names, cover_dir):
  # need to download as jumber of covers and then give the name from file names
  cover_urls = correctly_indexed_cover_urls(file_names, cover_urls)

  print("Downloading covers")
  cover_paths = []
  for cover, file in zip(cover_urls, file_names):
    try: 
      response = requests.get(cover, stream=True)
      response.raise_for_status()
      cover_path = os.path.join(cover_dir, file + cover[-4:])
      cover_paths.append(cover_path)
      open(cover_path, 'wb').write(response.content)
    except requests.exceptions.RequestException as e:
      print(f"Error downloading image: {e}")
  
  print("Downloaded all covers")
  return sorted(cover_paths)


def main(anime: str, file_names):
  cover = tmp.TempDir()
  cover_dir = cover.make_tempdir(".tmp_covers")

  manga_url = get_manga_url(anime) # eventually have a way to pick which urls are best
  cover_urls = get_img_urls(manga_url)
  cover_paths = download_covers(cover_urls, sorted(file_names), cover_dir)

  # gets volumes so I cna use them
  return cover, cover_dir
    

    # need to download the cover and then edit the meta of the volumes 
    # could make a tmp to do this (so make a file with the tmp so that I can use it everywhere)

# anime = 'jagaaaaaa'
# file_names = ["ligma_c051_c100", "ligma_c101_c150", "ligma_c151_c200"] # <- is var archive_names
# cover_count = 2
# main(anime, file_names) 



 
# todo:
# - get cover image
# - edit file data with: 
#     - author
#     - amazon ibn