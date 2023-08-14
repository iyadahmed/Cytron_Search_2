import pickle
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from tqdm import trange
from webdriver_manager.chrome import ChromeDriverManager

from crawler_state import CrawlerState

MAX_PAGES = 11
MAX_URL_PROGRESS_BAR_STRING_LENGTH = 50


# https://web.archive.org/web/20230814145816/https://www.selenium.dev/blog/2023/headless-is-going-away/
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)

crawler_state_path = Path(__file__).parent / "crawler_state.bin"

if crawler_state_path.exists():
    with open(crawler_state_path, "rb") as file:
        state: CrawlerState = pickle.load(file)
else:
    state = CrawlerState()
    state.urls_queue.append("https://www.wikipedia.org/")


for _ in (pbar := trange(MAX_PAGES)):
    if len(state.urls_queue) == 0:
        break
    url = state.urls_queue.pop()
    assert url not in state.visited_urls
    state.visited_urls.add(url)

    pbar.set_description(
        f"Visiting {url[:MAX_URL_PROGRESS_BAR_STRING_LENGTH]}"
        + ("..." * (len(url) > MAX_URL_PROGRESS_BAR_STRING_LENGTH))
    )

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, features="lxml")
    clean_text = soup.get_text()

    for word in clean_text.split():
        state.engine_index[word.lower()].add(url)

    for e in driver.find_elements(By.CSS_SELECTOR, "a[href]"):
        sub_url = e.get_attribute("href")
        assert sub_url is not None
        if sub_url in state.visited_urls:
            continue
        state.urls_queue.append(sub_url)

driver.quit()


# Save crawler state
with open(crawler_state_path, "wb") as file:
    pickle.dump(state, file)
