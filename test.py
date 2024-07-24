from utils.utils import *
def main(anime):
    search_found = False
    while not search_found:
        search_query = f"{anime}"
        try:
            # wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            # title = driver.title
            # print(title)

            # search = driver.find_element(By.ID, "twotabsearchtextbox")
            # search.clear()
            # search.send_keys(search_query)
            # search_button = driver.find_element(By.ID, "nav-search-submit-button")
            # search_button.click()

            # wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "puisg-col-inner")))
            # amazon_containers = driver.find_elements(By.CLASS_NAME, "puisg-col-inner")
            amazon = Search()
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
            user_choice = input("Search failed. Retry (y/n) or enter new name: ").lower()
            if user_choice == 'n':
                break 
            else:
                anime = user_choice
        print("Urls successfully found")
        amazon.quit()
        try:
            return link
        except IndexError:
            print("Cant find that anime")
            print("Relaunch using the flag --imgs")
            exit()

print(main("berserk"))