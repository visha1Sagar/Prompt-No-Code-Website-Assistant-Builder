import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

async def fetch_content(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content

def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text()
    cleaned_text = re.sub(r'\n+', '\n', text).strip()
    return cleaned_text

async def main():
    url = "https://nust.edu.pk/"
    html = await fetch_content(url)
    text = bs4_extractor(html)
    print(text[:500])  # Print the first 500 characters of the extracted text

if __name__ == "__main__":
    asyncio.run(main())
