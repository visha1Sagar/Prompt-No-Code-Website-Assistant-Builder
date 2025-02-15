import asyncio
import json
import re
import traceback
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from urllib.parse import urljoin, urlparse
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Define your markdown generator.
md_generator = DefaultMarkdownGenerator(
    options={
        "ignore_links": True,
        "ignore_images": True,
        "escape_html": False,
    }
)

# Create a run configuration.
run_config = CrawlerRunConfig(
    markdown_generator=md_generator,
    cache_mode=CacheMode.BYPASS,
)

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
        traceback.print_exc()
        return None

    try:
        print(f"\nFetched content from: {url}")
        print(result.cleaned_html[:200])
        
        if url.lower().endswith((".doc", ".img", ".png", ".pdf", ".docx")):
            return None

        child_urls = set()
        if depth < max_depth:
            for link in result.links.get("internal", []):
                full_url = urljoin(url, link["href"])
                if urlparse(full_url).netloc == base_domain and full_url not in visited:
                    child_urls.add(full_url)

        markdown_content = ""
        try:
            if result.markdown_v2 and result.markdown_v2.raw_markdown:
                markdown_content = result.markdown_v2.raw_markdown
            elif result.markdown:
                markdown_content = result.markdown
            else:
                print(f"No markdown available for {url}.")
        except Exception as e:
            print(f"Error processing markdown for {url}: {e}")
            traceback.print_exc()

        if markdown_content:
            try:
                cleaned_markdown = remove_images(markdown_content)
            except Exception as e:
                print(f"Error cleaning markdown for {url}: {e}")
                traceback.print_exc()
                cleaned_markdown = markdown_content
        else:
            cleaned_markdown = ""

        pages_data[url] = {
            "markdown": cleaned_markdown,
            "child_urls": list(child_urls)
        }

        if depth < max_depth:
            tasks = [
                crawl_page(crawler, child_url, base_domain, depth + 1, max_depth, visited, pages_data)
                for child_url in child_urls
            ]
            await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(f"Unexpected error processing {url}: {e}")
        traceback.print_exc()
    
    return url

async def call_crawler(start_url: str = "https://nust.edu.pk", output_file: str = "crawl_results.json"):
    base_domain = urlparse(start_url).netloc
    visited = set()
    pages_data = {}
    
    async with AsyncWebCrawler() as crawler:
        print("Browser should launch now...")
        await crawl_page(crawler, start_url, base_domain, depth=0, max_depth=3, visited=visited, pages_data=pages_data)
    
    final_output = {
        "root": start_url,
        "pages": pages_data
    }
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=2, ensure_ascii=False)
        print(f"Crawl data saved to {output_file}")
    except Exception as e:
        print(f"Error saving crawl data: {e}")
        traceback.print_exc()
    
    return output_file

if __name__ == "__main__":
    asyncio.run(call_crawler())