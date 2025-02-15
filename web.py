import asyncio
import re
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader

# Define the extractor function
def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text()
    cleaned_text = re.sub(r'\n+', '\n', text).strip()
    return cleaned_text

# Define the function to fetch documents
async def fetch_docs():
    # Initialize the RecursiveUrlLoader with the specified parameters
    loader = RecursiveUrlLoader(
        "https://nust.edu.pk/",
        max_depth=3,
        use_async=True,
        extractor=bs4_extractor,
        exclude_dirs=(
            # Add directories or file extensions to exclude binary files
            '.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.avi', '.mov', '.pdf', '.docx', '.xlsx'
        ),
        # Additional parameters can be set as needed
        # timeout=10,
        # check_response_status=True,
        # continue_on_failure=True,
        # prevent_outside=True,
        # base_url=None,
    )
    
    # Load the documents asynchronously
    docs = await loader.aload()
    
    # Process and print the content of each document
    for doc in docs:
        print(doc.page_content[:500])  # Print the first 500 characters of the page content
        print(doc.metadata)            # Print the metadata of the document

# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(fetch_docs())
