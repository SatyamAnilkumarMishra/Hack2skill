from duckduckgo_search import DDGS

with DDGS() as ddgs:
    results = ddgs.text("which is best collage in india give e name?", max_results=2)
    for r in results:
        print(r["title"], ":", r["href"])

