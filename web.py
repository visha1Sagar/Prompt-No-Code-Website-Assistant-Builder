import asyncio
from langchain_community.document_loaders import RecursiveUrlLoader
import re
from bs4 import BeautifulSoup


def fetch_docs():
    loader = RecursiveUrlLoader(
    "https://netsoltech.com/",
    max_depth=3,
    use_async=True,
    extractor=bs4_extractor
    # metadata_extractor=None,
    # exclude_dirs=(),
    # timeout=10,
    # check_response_status=True,
    # continue_on_failure=True,
    # prevent_outside=True,
    # base_url=None,
    # ...
    )
    # docs_lazy = loader.load()  # Correct use of await inside async function
    print(loader.load()[0].page_content[:500])
    # docs = [doc for doc in docs_lazy]
    # print(len(docs))
    # return docs[0].page_content
    # for doc in docs:
    #     print(doc.page_content[:100])
    #     print(doc.metadata)
        
        
def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text()
    cleaned_text = re.sub(r'\n+', '\n', text).strip()
    return cleaned_text


# Run the async function
html = fetch_docs()
# print(bs4_extractor(html))


