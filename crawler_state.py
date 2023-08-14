from collections import defaultdict


class CrawlerState:
    def __init__(self):
        self.engine_index: defaultdict[str, set[str]] = defaultdict(set)
        self.visited_urls: set[str] = set()
        self.urls_queue: list[str] = []
