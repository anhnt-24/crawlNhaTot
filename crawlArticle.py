import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from webdriver_manager.chrome import ChromeDriverManager

link_list = []
try:
    for page in range(126, 150):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/124.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        url = f"https://www.nhatot.com/mua-ban-bat-dong-san-ha-noi?page={page}"
        print(f"Đang lấy: {url}")
        driver.get(url)
        time.sleep(3)

        ul_element = driver.find_element(By.CLASS_NAME,"list-view")
        lis = ul_element.find_elements(By.TAG_NAME, "li")
        for li in lis:
            a=li.find_element(By.TAG_NAME, "a")
            href = a.get_attribute("href")
            if href and href.startswith("https://www.nhatot.com/"):
                print(href)
                link_list.append(href)
        driver.quit()

finally:
    unique_links = list(set(link_list))
    with open("alinks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Link"])  # header
        for link in unique_links:
            writer.writerow([link])
