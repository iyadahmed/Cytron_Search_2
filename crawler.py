from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

MAX_PAGES = 11

# https://web.archive.org/web/20230814145816/https://www.selenium.dev/blog/2023/headless-is-going-away/
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)

urls = ["https://www.wikipedia.org/"]
visited = set()

for _ in range(MAX_PAGES):
    if len(urls) == 0:
        break
    url = urls.pop()
    assert url not in visited
    visited.add(url)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, features="lxml")
    clean_text = soup.get_text()
    print(clean_text)
    # TODO: split clean text into words and index web page to search it later

    for e in driver.find_elements(By.CSS_SELECTOR, "a[href]"):
        sub_url = e.get_attribute("href")
        assert sub_url is not None
        if sub_url in visited:
            continue
        urls.append(sub_url)

driver.quit()
