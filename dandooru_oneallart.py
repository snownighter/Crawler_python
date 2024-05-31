from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import os

author_name = 'author_name'
pages = 1

# WebDriver
driver_path = 'D:\chromedriver-win64\chromedriver.exe'
options = Options()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# URL
driver.get('https://danbooru.donmai.us')

page_number = page = 1
while page_number <= pages:
    # Artist's page
    driver.get(f'https://danbooru.donmai.us/posts?tags={author_name}&page={page_number}')
    time.sleep(0.5)

    # Get the URLs of all artworks
    artwork_elements = driver.find_elements(By.XPATH, '//a[@class="post-preview-link"]')
    artwork_urls = [element.get_attribute('href') for element in artwork_elements]
    print(f"Find the artwork URL {artwork_urls}")

    def download_image(image_url, save_path):
        # headers_download = {"referer": "https://danbooru.donmai.us/"}
        for ext in ['.png', '.jpg']:
            original_url = image_url[:-4] + ext
            response = requests.get(url=original_url)
            if response.status_code == 200:
                with open(save_path + ext, 'wb') as handler:
                    handler.write(response.content)
                print(f"Image downloaded successfully as {save_path + ext}")
                return
        print(f"Failed to download image from {image_url}")

    for artwork_url in artwork_urls:
        # URL
        driver.get(artwork_url)
        time.sleep(0.2)

        view_original = driver.find_elements(By.XPATH, '//a[contains(@class, "image-view-original-link")]')
        if view_original:
            image_url = view_original[0].get_attribute('href')
        elif driver.find_elements(By.XPATH, '//video[contains(@class, "fit-width")]'):
            page += 1
            continue
        else:
            image_element = driver.find_elements(By.XPATH, '//img[contains(@class, "fit-width")]')
            image_url = image_element[0].get_attribute('src')

        # Create a directory
        if not os.path.exists(f'{author_name}_images'):
            os.makedirs(f'{author_name}_images')

        # Save
        if 'original' in image_url:
            image_name = f"{author_name}_images/{author_name}_{page}"
            page += 1
            download_image(image_url, image_name)

    page_number += 1

print("Finished.")
