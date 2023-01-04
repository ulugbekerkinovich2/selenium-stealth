import json
from selenium import webdriver
import selenium.common.exceptions as exc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.headless = True
driver = webdriver.Chrome(options=options)

stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)

data = {}

for page in range(1, 3):
        url = f"https://www.russiadiscovery.ru/tours/trekkingi/?page={page}"
        driver.get(url)

        # Извлекаем все блоки со страницы
        blocks = driver.find_element(By.CLASS_NAME, "tourListUl")
        posts = blocks.find_elements(By.TAG_NAME, "li")

        for post in posts:
                title = post.find_element(By.CLASS_NAME, "tourList__title").find_element(By.TAG_NAME, "a").text
                title_link = post.find_element(By.CLASS_NAME, "tourList__title").find_element(By.TAG_NAME, "a").get_attribute("href")
                price = post.find_element(By.CLASS_NAME, "tourList__price").find_element(By.TAG_NAME, "span").text.replace(" ", ".")
                data[title] = {
                        "url": title_link,
                        "price": price
                }

for post_url in data.values():
        driver.get(post_url['url'])
        print(f"Обрабатываем: {post_url['url']}")

        try:
                group_size = driver.find_element(By.CSS_SELECTOR, "#rele_one > div.tourPage__main__sidebar.right_booking_tour > div:nth-child(4) > div.size_group > div.right").text
                post_url['group_size'] = group_size
        except exc.NoSuchElementException:
                print("Объект group_size не найден")
                post_url['group_size'] = "не найден"

        photos_count = driver.find_element(By.CLASS_NAME, "moreMediaGallery").text
        photos_count = int(photos_count.replace("+", "").replace(" ", "")) + 5
        post_url["photos"] = []

        for photo_num in range(1, photos_count):
                photo_url = f"{post_url['url']}#&gid=1&pid={photo_num}"
                post_url["photos"].append(photo_url)

with open("result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)