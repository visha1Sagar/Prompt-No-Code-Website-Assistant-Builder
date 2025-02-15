import re

def remove_header_footer(markdown_text):
    regex = r"^.*?(?=\n# )"
    cleaned_text = re.sub(regex, '', markdown_text, flags=re.DOTALL)
    return cleaned_text

# Example usage:
import json

with open("crawl_netsol.json", "r", encoding="utf-8") as f:
    crawl_results = json.load(f)

# Extract the markdown content from the crawl results
markdown_text = [page["markdown"] for page in crawl_results["pages"].values()]


cleaned_markdown = remove_header_footer(markdown_text[3])
print(cleaned_markdown)
