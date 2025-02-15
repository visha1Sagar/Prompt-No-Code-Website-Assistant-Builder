import asyncio
import json
from crawl4ai import AsyncWebCrawler
from urllib.parse import urljoin, urlparse

async def crawl_page(crawler, url, base_domain, depth, max_depth, visited):
    # Skip URLs that have already been visited to avoid cycles
    if url in visited:
        return None
    visited.add(url)
    try:
        result = await crawler.arun(url=url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

    print(f"Fetched content from: {url}")
    print(result.markdown[:200])  # Print the first 200 characters for brevity

    # Create a dictionary for the current page
    page_data = {
        "url": url,
        "markdown": result.markdown,
        "children": []
    }

    # Only continue if we haven't reached the max_depth
    if depth < max_depth:
        internal_links = set()
        for link in result.links.get("internal", []):
            full_url = urljoin(url, link["href"])
            if urlparse(full_url).netloc == base_domain and full_url not in visited:
                internal_links.add(full_url)
        # Recursively crawl all discovered internal links concurrently
        tasks = [
            crawl_page(crawler, child_url, base_domain, depth + 1, max_depth, visited)
            for child_url in internal_links
        ]
        children_results = await asyncio.gather(*tasks)
        page_data["children"] = [child for child in children_results if child is not None]

    return page_data

async def main():
    start_url = "https://nust.edu.pk/"
    base_domain = urlparse(start_url).netloc
    visited = set()
    async with AsyncWebCrawler() as crawler:
        # Start at depth 0; here max_depth is set to 3
        root_data = await crawl_page(crawler, start_url, base_domain, depth=0, max_depth=2, visited=visited)
    
    # Save the resulting JSON structure to a file for analysis
    with open("crawl_results.json", "w", encoding="utf-8") as f:
        json.dump(root_data, f, indent=2, ensure_ascii=False)
    print("Crawl data saved to crawl_results.json")

if __name__ == "__main__":
    asyncio.run(main())
