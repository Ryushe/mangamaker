# this file will handle the metadata of the file, eg: get the manga pics, apply those pics to the cbz file, add the amazin ibn number, author, etc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


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

def getUrl(anime): 
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://mangadex.org/")
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.ID, "header-search-input")))
    except:
        print("page failed to load, retrying")
        getUrl(anime)
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

def get_covers(url):
    driver = webdriver.Chrome()
    driver.get(url+"?tab=art")
    wait = WebDriverWait(driver, 10) 
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "subtitle")))

    cover_images = driver.find_elements(By.CSS_SELECTOR, "img[data-v-2763eefc]")

    img_srcs = []

    for img in cover_images:
        img_srcs.append(img.get_attribute("src"))
    return img_srcs[1:] # removes the shown cover (when u search the item)


def main(anime):
    url = getUrl(anime) # eventually have a way to pick which urls are best
    covers = get_covers(url)

    # need to download the cover and then edit the meta of the volumes 
    # could make a tmp to do this (so make a file with the tmp so that I can use it everywhere)

anime = 'jagaaaaaa'
main(anime) 
 
# todo:
# - get cover image
# - edit file data with: 
#     - author
#     - amazon ibn