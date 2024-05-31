from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

USERNAME = 'my_user'
PASSWORD = 'my_password'
artist_page_url = 'https://www.pixiv.net/users/<author_id>/artworks?p='
pages, scrolls = 1, 1

# WebDriver
driver_path = 'D:\chromedriver-win64\chromedriver.exe'
options = Options()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(executable_path=driver_path, options=options)

try:
    # Pixiv Login URL
    driver.get('https://accounts.pixiv.net/login')

    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username" or @placeholder="信箱地址或pixiv ID"]')))
    username_field.send_keys(USERNAME)

    password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="current-password" or @placeholder="密碼"]')))
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # reCAPTCHA
    try:
        recaptcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="g-recaptcha-bubble-arrow"]'))
        )
        print("Please solve the reCAPTCHA manually.")
        input("Press Enter to continue after solving the reCAPTCHA...")
    except:
        pass

    wait.until(EC.url_to_be('https://www.pixiv.net/'))
    
    if driver.current_url == 'https://www.pixiv.net/':
        print("Success!")

        page_number = 1
        while page_number <= pages:
            # Artist's page
            driver.get(f'{artist_page_url}{page_number}')
            time.sleep(1)

            author_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//h1[@class="sc-1bcui9t-5 ibhMns"]')))
            author_name = author_name.text

            # Get the URLs of all artworks
            artwork_elements = driver.find_elements(By.XPATH, '//a[@class="sc-d98f2c-0 sc-rp5asc-16 iUsZyY sc-bdnxRM fGjAxR"]')
            artwork_urls = [element.get_attribute('href') for element in artwork_elements]
            print(f"Find the artwork URL {artwork_urls}")

            def download_image(image_url, save_path):
                headers_download = {"referer": "https://www.pixiv.net/"}
                for ext in ['.png', '.jpg', '.gif']:
                    original_url = image_url.replace('img-master', 'img-original').split('_master')[0] + ext
                    response = requests.get(url=original_url,headers=headers_download)
                    if response.status_code == 200:
                        with open(save_path + ext, 'wb') as handler:
                            handler.write(response.content)
                        print(f"Image downloaded successfully as {save_path + ext}")
                        return
                print(f"Failed to download image from {image_url}")

            for page, artwork_url in enumerate(artwork_urls):
                # URL
                driver.get(artwork_url)
                time.sleep(0.5)
            
                try:
                    view_more_button = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, '//button[@class="sc-emr523-0 guczbC"]/div[contains(text(), "查看全部")]'))
                    )
                    if view_more_button:
                        first_image_element = driver.find_element(By.XPATH, '//img[contains(@class, "eMdOSW")]')
                        actions = ActionChains(driver)
                        actions.move_to_element(first_image_element).click().perform()
                        time.sleep(1)

                        # Scroll to load all images
                        scroll_count = 0
                        while scroll_count < scrolls:
                            driver.execute_script("window.scrollBy(0, 2*window.innerHeight);")
                            scroll_count += 1
                            time.sleep(0.1)
                except Exception as e:
                    pass
                    # print("No button found or failed to click it:", e)

                image_elements = driver.find_elements(By.XPATH, '//img[contains(@class, "eMdOSW")]')
                
                # Create a directory
                if not os.path.exists(f'{author_name}_images'):
                    os.makedirs(f'{author_name}_images')

                # Save
                image_counter = 1
                for image_element in image_elements:
                    image_url = image_element.get_attribute('src')
                    if 'img-master' in image_url:
                        image_name = f"{author_name}_images/{author_name}_{page+1+48*(page_number-1)}_{image_counter}"
                        download_image(image_url, image_name)
                        image_counter += 1

            page_number += 1
        
        print("Finished.")
    else:
        print("Fail.")
finally:
    driver.quit()
