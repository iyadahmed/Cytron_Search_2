import mmap
from struct import Struct

import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

long_long_packer = Struct("q")

options = webdriver.ChromeOptions()
# https://web.archive.org/web/20230814145816/https://www.selenium.dev/blog/2023/headless-is-going-away/
options.add_argument("--headless=new")
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)


driver.get("https://www.wikipedia.org/")


# Index page content
clean_text = BeautifulSoup(driver.page_source, "lxml").get_text()
with open("hashed_keywords.bin", "wb") as file:
    for keyword in clean_text.split():
        keyword_hash = hash(keyword.lower())
        data = long_long_packer.pack(keyword_hash)
        file.write(data)


with open("hashed_keywords.bin", "r+b") as file:
    mm = mmap.mmap(file.fileno(), 0)
    arr = np.ndarray.__new__(
        np.ndarray, buffer=mm, dtype=np.int64, shape=(mm.size() // 8,)
    )
    arr.sort(kind="heapsort")


# Search for a keyword
with open("hashed_keywords.bin", "r+b") as file:
    mm = mmap.mmap(file.fileno(), 0)
    arr = np.ndarray.__new__(
        np.ndarray, buffer=mm, dtype=np.int64, shape=(mm.size() // 8,)
    )
    query = hash("google")
    i = arr.searchsorted(query)
    print(arr[i] == query)

# Find all links
link_elements = driver.find_elements(By.TAG_NAME, "a")
for e in link_elements:
    try:
        link = e.get_attribute("href")
    except Exception:
        continue

driver.quit()
