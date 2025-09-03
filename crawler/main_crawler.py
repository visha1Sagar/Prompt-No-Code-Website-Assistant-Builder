import asyncio
import json
import re
from urllib.parse import urljoin, urlparse
import requests
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import PyPDF2
from io import BytesIO
import traceback


def extract_pdf_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad HTTP response

        # Read PDF in memory using PyPDF2
        pdf_file = BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Check if PDF is encrypted
        if pdf_reader.is_encrypted:
            pdf_reader.decrypt("")  # Try unlocking

        # Extract text safely
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        if not text.strip():  # Check if text extraction failed (PDF might be scanned)
            text = ""

        return text

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        traceback.print_exc()  # Print full error details
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()  # Print full error details
        traceback.print_exc()

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

# Create a run configuration.
run_config = CrawlerRunConfig(
    markdown_generator=md_generator,
    # pdf=True,
    cache_mode=CacheMode.BYPASS,
    # scan_full_page=True,
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
        return None

    print(f"\nFetched content from: {url}")
    
    # Extract child URLs only if we haven't reached max_depth.
    child_urls = set()
    if depth < max_depth:
        for link in result.links.get("internal", []):
            full_url = urljoin(url, link["href"])
            if urlparse(full_url).netloc == base_domain and full_url not in visited:
                child_urls.add(full_url)
    
    # Process the result based on URL type.
    # If the URL indicates a PDF file, we use the PDF bytes.
    if url.lower().endswith(".pdf"):
        try:
            print("The URL contains pdf.")
            pdf_text = extract_pdf_text(url)
            print(pdf_text[:100])
            # import pdb; pdb.set_trace()
            pages_data[url] = {
            "markdown": pdf_text,
            "child_urls": list(child_urls)
            }
            
        except Exception as e:
            print(f"Error processing pdf for {url}: {e}")
    elif (url.lower().endswith((".doc", ".jpg", ".png", ".docx")) or any(substring in url.lower() for substring in ("img", ".jpg"))):
        # Skip non-text documents.
        return
    else:
        # For text-based pages, try to extract markdown.
        markdown_content = ""
        try:
            # Use the current markdown attribute which returns a MarkdownGenerationResult
            if hasattr(result, 'markdown') and result.markdown:
                # Check if it's the new MarkdownGenerationResult object
                if hasattr(result.markdown, 'raw_markdown'):
                    markdown_content = result.markdown.raw_markdown
                elif isinstance(result.markdown, str):
                    markdown_content = result.markdown
                else:
                    # Fallback to string representation
                    markdown_content = str(result.markdown)
            else:
                print(f"No markdown available for {url}.")
        except Exception as e:
            print(f"Error processing markdown for {url}: {e}")
            # Try to get basic text content as fallback
            try:
                if hasattr(result, 'cleaned_html'):
                    markdown_content = result.cleaned_html
                elif hasattr(result, 'html'):
                    markdown_content = result.html
            except Exception as fallback_e:
                print(f"Fallback content extraction also failed for {url}: {fallback_e}")
        
        # Remove image markdown syntax if content is available.
        if markdown_content:
            try:
                cleaned_markdown = remove_images(markdown_content)
            except Exception as e:
                print(f"Error cleaning markdown for {url}: {e}")
                cleaned_markdown = markdown_content
        else:
            cleaned_markdown = ""
        
        print("The URL contains text.")
        print(cleaned_markdown)
        pages_data[url] = {
            "markdown": cleaned_markdown,
            "child_urls": list(child_urls)
        }
    
    # Recursively crawl each child URL if within max_depth.
    if depth < max_depth:
        tasks = [
            crawl_page(crawler, child_url, base_domain, depth + 1, max_depth, visited, pages_data)
            for child_url in child_urls
        ]
        # Use return_exceptions=True so that one failing page doesn't break the entire crawl.
        await asyncio.gather(*tasks, return_exceptions=True)
    
    return url

async def call_crawler(start_url: str = "https://nust.edu.pk", output_file: str = "crawl_results.json"):
    base_domain = urlparse(start_url).netloc
    visited = set()
    pages_data = {}  # This will map each URL to its details.

    # Create a BrowserConfig with desired options.

    # Pass the browser config using the 'browser_config' keyword.
    async with AsyncWebCrawler() as crawler:
        print("Browser should launch now...")
        await crawl_page(crawler, start_url, base_domain, depth=0, max_depth=4, visited=visited, pages_data=pages_data)

    # Final output structure: a root URL and a dictionary of pages.
    final_output = {
        "root": start_url,
        "pages": pages_data
    }

    # Save the JSON to a file for later analysis.
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    print(f"Crawl data saved to {output_file}")
    return output_file

if __name__ == "__main__":
    asyncio.run(call_crawler("https://lums.edu.pk/"))
