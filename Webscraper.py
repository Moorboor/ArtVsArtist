import os
from selenium import webdriver
from selenium.webdriver.common.by import By 
from Credentials import username, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from icecream import ic
from tqdm import tqdm
import requests

ABS_PATH = os.path.abspath("")
DOWNLOAD_PATH = os.path.join(ABS_PATH, "downloads")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


class InstaScraper():

    def __init__(self, username, password):

        self.driver = webdriver.Chrome()
        self.password = password
        self.username = username
        self.source = "https://www.instagram.com/"


    def login(self):
        self.driver.get(self.source)
        try:
            self.cookie_decline_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"))
            )
            self.cookie_decline_btn.click()
        except Exception as e:
            print(f"Cookie decline button not found or not clickable: {e}")

        self.username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username")))
        self.username_field.send_keys(self.username)
        self.password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password")))
        self.password_field.send_keys(self.password)
        self.login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        time.sleep(3)
        self.login_btn.click()
        time.sleep(10)
    

    def get_hrefs(self):
        href_links_list = []
        while True:
            link_elements = self.driver.find_elements(By.CLASS_NAME, "x1i10hfl")
            href_links = [link.get_attribute("href") for link in link_elements if link.get_attribute("href") and ("/p/" in link.get_attribute("href"))]
            new_links = set(href_links).difference(set(href_links_list))
            if not new_links:
                break            
            href_links_list.extend(new_links)

            self.driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(2.5)
            
        return href_links_list


    def search_url(self, *, url):
        self.driver.get(url)
        self.driver.implicitly_wait(4)
    

    def scrape_website(self, *, url):

        post_id = f"{url.split('/p/')[1]}"
        POST_PATH = os.path.join(DOWNLOAD_PATH, post_id)
        os.makedirs(POST_PATH, exist_ok=True)

        try:
            likes_count = self.driver.find_element(By.XPATH, "//*[contains(text(), 'likes')]").text
            date = self.driver.find_element(By.CLASS_NAME, "_aaqe").text
            post_content = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/span").text

            ic(url, likes_count, date)
            
            with open(f"{os.path.join(POST_PATH, 'scraped_data')}.txt", "w") as f:
                f.write(f"Date: {date}\n")
                f.write(f"Likes: {likes_count}\n")
                f.write(f"Content: {post_content}\n")
        except Exception as e:
            ic(f"An error occurred{e}")
        
        try:
            image_elements = self.driver.find_elements(By.XPATH, "//img")
            image_urls = [img.get_attribute("src") for img in image_elements]
            self.download_images(post_id=post_id, image_urls=image_urls)
        except Exception as e:
            ic(f"An error occurred{e}")


    def download_images(self, *, post_id, image_urls):

        for i, image_url in enumerate(image_urls):
            if i!=3:
                continue
            try:
                response = requests.get(url=image_url)
                with open(f"{os.path.join(DOWNLOAD_PATH, post_id, f'IMG{i}')}.jpg", "wb") as f:
                    f.write(response.content)
            except Exception as e:
                ic(f"An error occurred{e}")

    def close_browser(self):
        self.driver.quit()


            
insta = InstaScraper(username=username, 
                     password=password)
insta.login()
insta.search_url(url="https://www.instagram.com/artvsartist/")
href_links_list = insta.get_hrefs()


for href in tqdm(href_links_list):
    insta.search_url(url=href)
    insta.scrape_website(url=href)    
    