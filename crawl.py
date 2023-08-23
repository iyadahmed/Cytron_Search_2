import csv
from collections import deque
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService

gecko_path = (Path(__file__).parent / "geckodriver").as_posix()
gecko_options = webdriver.FirefoxOptions()
gecko_options.add_argument("--headless")
gecko_service = FirefoxService(gecko_path, log_output="geckodriver.log")
gecko_driver = webdriver.Firefox(service=gecko_service, options=gecko_options)

urls_queue: deque[str] = deque(["https://www.wikipedia.org/"])
visited_urls: set[str] = set()
with open("crawl_result.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["text", "url"])

    def crawl(url: str):
        if url in visited_urls:
            return
        visited_urls.add(url)
        print(f"Visiting {url}")
        gecko_driver.get(url)

        clean_text = BeautifulSoup(gecko_driver.page_source, "lxml").get_text(
            separator=" ", strip=True
        )
        csv_writer.writerow([clean_text, url])

        # Find all links
        link_elements = gecko_driver.find_elements(By.TAG_NAME, "a")
        for e in link_elements:
            try:
                link = e.get_attribute("href")
                if link is not None:
                    urls_queue.append(link)
            except Exception:
                continue

    while len(urls_queue) > 0:
        crawl(urls_queue.popleft())

    gecko_driver.quit()
