import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.edge.options import Options
cnt=0
def crawl_nhatot_detail(url):
    global cnt
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
    driver = webdriver.Edge(options=options)

    try:
        result={}
        driver.get(url)
        time.sleep(3)  # vẫn giữ sleep
        price = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/div[3]/div/div/b').text
        published_at = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[4]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/div[4]/div[2]/span').text

        now = datetime.now().isoformat()
        result['now'] = now
        result['published_at'] = published_at
        result['price'] = price

        table = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[1]/div/div[2]/div[2]/div/div[3]/div/div')
        items = table.find_elements(By.CSS_SELECTOR, '[data-testid="param-item"]')
        for item in items:
            element = item.find_element(By.TAG_NAME, 'strong')
            text = element.text
            tag = element.get_attribute('itemprop')
            result[tag] = text

        print(result)
        cnt+=1
        print("Lần thứ",cnt)
        return result
    finally:
        driver.quit()

csv_file = "links.csv"
df = pd.read_csv(csv_file)
links = df['Link'].dropna().tolist()

results = []
max_workers = 5
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_url = {executor.submit(crawl_nhatot_detail, link): link for link in links[:10]}
    for future in as_completed(future_to_url):
        try:
            data = future.result()
            if data:
                results.append(data)
        except Exception as e:
            print("Lỗi khi crawl:", e)

df_results = pd.json_normalize(results)
df_results.to_csv("results.csv", index=False, encoding="utf-8-sig")

print("Hoàn tất lưu CSV, số dòng:", len(df_results))
