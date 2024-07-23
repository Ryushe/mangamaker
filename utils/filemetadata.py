# this file will handle the metadata of the file, eg: get the manga pics, apply those pics to the cbz file, add the amazin ibn number, author, etc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import tmp 
import re
import os


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

def get_manga_url(anime): 
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://mangadex.org/")
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.ID, "header-search-input")))
    except:
        print("page failed to load, retrying")
        get_manga_url(anime)
    title = driver.title
    print(title)
    search = driver.find_element(By.ID, "header-search-input")
    search.send_keys(anime)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "dense-manga-container")))
    manga_containers = driver.find_elements(By.CLASS_NAME, "dense-manga-container")

    potential_urls = []
    for manga in manga_containers:
        web_manga_name = manga.find_element(By.TAG_NAME, "div").text
        if(is_similar(anime, web_manga_name)):
            potential_urls.append(manga.find_element(By.TAG_NAME, "a").get_attribute("href"))
    driver.close()
    return potential_urls[0]

def get_img_urls(url):
    driver = webdriver.Chrome()
    driver.get(url+"?tab=art")
    wait = WebDriverWait(driver, 10) 
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "subtitle")))

    cover_urls = driver.find_elements(By.CSS_SELECTOR, "img[data-v-2763eefc]")

    img_srcs = []

    for img in cover_urls:
        img_srcs.append(img.get_attribute("src"))
    return img_srcs[1:] # removes the shown cover (when u search the item)
    

def extract_numbers(string):
  numbers = re.findall(r'\d+', string)
  return [int(num) for num in numbers]
  

def get_indexes(file_names):
  extracted_int = extract_numbers(file_names[0])
  chapters_per = max(extracted_int) - min(extracted_int) + 1
  start_index = min(extracted_int) // chapters_per  
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

 
def download_covers(cover_urls, file_names):
  # need to download as jumber of covers and then give the name from file names
  cover_imgs = tmp.TempDir()
  cover_dir = cover_imgs.make_tempdir('.tmp_covers')
  cover_urls = correctly_indexed_cover_urls(file_names, cover_urls)

  # fix below (not doing anything rn)
  for cover, file in zip(cover_urls, file_names):
    try: 
      response = requests.get(cover, stream=True)
      response.raise_for_status()
      cover_path = os.path.join(cover_dir, file + cover[-4:])
      open(cover_path, 'wb').write(response.content)
    except requests.exceptions.RequestException as e:
      print(f"Error downloading image: {e}")


def main(anime, file_names):
    manga_url = get_manga_url(anime) # eventually have a way to pick which urls are best
    cover_urls = get_img_urls(manga_url)
    download_covers(cover_urls, sorted(file_names))
    

    # need to download the cover and then edit the meta of the volumes 
    # could make a tmp to do this (so make a file with the tmp so that I can use it everywhere)

anime = 'jagaaaaaa'
file_names = ["ligma_c051_c100", "ligma_c101_c150", "ligma_c001_c050"] # <- is var title
cover_count = 2
main(anime, file_names) 



 
# todo:
# - get cover image
# - edit file data with: 
#     - author
#     - amazon ibn