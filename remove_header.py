from ask_openai import ask_openai
import json
import ast

def generate_regex(file_name):

    with open(file_name, "r", encoding="utf-8") as f:
        crawl_results = json.load(f)

    # Extract the markdown content from the crawl results
    markdown_pages = [page["markdown"] for page in crawl_results["pages"].values()]


    # Create a structured prompt for GPT
    prompt = f"""
    I have extracted multiple Markdown pages from a website, and I want to remove the header while keeping the main content intact.

    Here are examples of Markdown pages:

    ---
    ### Page 1:
    {markdown_pages[0]}

    ---
    ### Page 2:
    {markdown_pages[1]}

    ---
    ### Page 3:
    {markdown_pages[2]}

    ---

    ### Task:
    1. Analyze the pattern in the headers across all these pages.
    2. Identify where the **main content begins**, typically at the **first Markdown heading (`#`, `##`, `###`, etc.)**.
    3. Generate a **generalized Python regex (`re` module)** that can remove such headers from any similar Markdown page.

    ### Requirements:
    - The regex should work **dynamically** for different Markdown pages.
    - It should **remove everything before the first Markdown heading** (e.g., `# Title`, `## Section`, `### Heading`).
    - The regex must be formatted in **Python `re` syntax**, ready for use in `re.sub()`.
    - **Do NOT hardcode any specific phrase**—it must work for different documents.
    - You MUST not give ``` jsons or code blocks in the response.

    Please provide **only** the final regex in the json format:
    ```json

        `regex`: 'your_regex_here'

    ```

    without the ''' or ``` code blocks.
    """

    output= ask_openai(prompt, 1000)
    output = ast.literal_eval(output)
    regex = output["regex"]
    # regex = f'r"{regex}"'
    print(f"Generated regex (1):  {regex}")
    return regex


import re

def remove_header_footer(crawl_file):

    regex = generate_regex(crawl_file)
    print(f"Generated regex: {regex}")
    with open(crawl_file, "r", encoding="utf-8") as f:
        crawl_results = json.load(f)

    # replace the markdown text with cleaned text
    for page in crawl_results["pages"].values():
        page["markdown"] = re.sub(regex, '', page["markdown"], flags=re.DOTALL)

    # crawl_file = crawl_file.replace(".json", "_cleaned.json")

    with open(crawl_file, "w", encoding="utf-8") as f:
        json.dump(crawl_results, f, indent=2, ensure_ascii=False)




if __name__ == "__main__":
    remove_header_footer("crawl_netsol.json")


    