import pickle
from pathlib import Path

from crawler_state import CrawlerState

# Load crawler state
crawler_state_path = Path(__file__).parent / "crawler_state.bin"
with open(crawler_state_path, "rb") as file:
    state: CrawlerState = pickle.load(file)

query = "Google"
result = set.intersection(*(state.engine_index[term.lower()] for term in query.split()))
print(result)
