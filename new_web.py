import asyncio
import json
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from urllib.parse import urljoin, urlparse
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# # Define a BrowserConfig for Firefox with headless off and verbose logging.
# base_browser = BrowserConfig(
#     browser_type="firefox",
#     headless=False,   # Set headless to False so you can see the browser window.
#     text_mode=True
# )
#
# debug_browser = base_browser.clone(
#     headless=False,
#     verbose=True      # Verbose mode prints additional debugging info.
# )

# run_config = CrawlerRunConfig()

# Define your markdown generator.
md_generator = DefaultMarkdownGenerator(
    options={
        "ignore_links": True,
        "ignore_images": True,
        "escape_html": False,
        # "skip_internal_links": True,
        # "body_width": 80
    }
)

# # Create a run configuration.
run_config = CrawlerRunConfig(
    markdown_generator=md_generator,
    # excluded_tags=["a"],
    cache_mode=CacheMode.BYPASS,
    # md_generator,
    # markdown_generator=md_generator,
    # only_text=True,
)

# config.viewport_width = 1280
# config.viewport_height = 720

# config.use_managed_browser = False

# Fix: add the missing attribute to the config.
# config.browser_type = "firefox"

def remove_images(markdown_text: str) -> str:
    """Remove markdown image syntax (e.g. ![alt](url)) from the text."""
    return re.sub(r'!\[.*?\]\(.*?\)', '', markdown_text)

async def crawl_page(crawler, url, base_domain, depth, max_depth, visited, pages_data):
    if url in visited:
        return None
    visited.add(url)
    try:
        result = await crawler.arun(url=url, config=run_config)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


    # cleaned_markdown = remove_images(result.markdown)
    print(f"\nFetched content from: {url}")
    # print(cleaned_markdown[:200])  # Preview first 200 characters
    print(result.cleaned_html[:200])

    # Extract child URLs only if we haven't reached max_depth.
    child_urls = set()
    if depth < max_depth:
        for link in result.links.get("internal", []):
            full_url = urljoin(url, link["href"])
            if urlparse(full_url).netloc == base_domain and full_url not in visited:
                child_urls.add(full_url)

    # Store the page details in the dictionary.
    pages_data[url] = {
        "markdown": result.markdown_v2.raw_markdown,
        "child_urls": list(child_urls)
    }

    # Recursively crawl each child URL.
    if depth < max_depth:
        tasks = [
            crawl_page(crawler, child_url, base_domain, depth + 1, max_depth, visited, pages_data)
            for child_url in child_urls
        ]
        await asyncio.gather(*tasks)
    
    return url

async def main(start_url: str, output_file: str = "crawl_results.json",):
    # start_url = "https://nust.edu.pk/"
    base_domain = urlparse(start_url).netloc
    visited = set()
    pages_data = {}  # This will map each URL to its details.

    # Pass your browser config using the 'browser_config' keyword and run config via config parameter.
    async with AsyncWebCrawler() as crawler:
        print("Browser should launch now...")
        # Set max_depth to 2 (or 3, as desired) for the recursive crawl.
        await crawl_page(crawler, start_url, base_domain, depth=0, max_depth=2, visited=visited, pages_data=pages_data)
    
    # Final output structure: a root URL and a dictionary of pages.
    final_output = {
        "root": start_url,
        "pages": pages_data
    }
    
    # Save the JSON to a file for later analysis.
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    print("Crawl data saved to crawl_results.json")

if __name__ == "__main__":
    asyncio.run(main("https://github.com/visha1Sagar"))
