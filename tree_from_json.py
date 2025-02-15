import json
from urllib.parse import urlparse

# Define a function to create a new tree node.
def new_node():
    return {"children": {}, "urls": []}

# Load the JSON data from a file named "data.json"
with open("crawl_results.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize a set for storing unique URLs.
url_set = set()

# Add the root URL if present.
if "root" in data:
    url_set.add(data["root"])

# Iterate through pages: add each page key and its child_urls.
pages = data.get("pages", {})
for key, page in pages.items():
    url_set.add(key)
    for child in page.get("child_urls", []):
        url_set.add(child)

# Build a tree structure that stores the URLs as data.
# The top-level keys will be the base domain (e.g., "https://nust.edu.pk")
tree = {}

def add_url_to_tree(url):
    parsed = urlparse(url)
    # Create a list of non-empty path segments.
    segments = [seg for seg in parsed.path.split("/") if seg]
    
    # Use the base domain (scheme + netloc) as the top-level key.
    base = f"{parsed.scheme}://{parsed.netloc}"
    if base not in tree:
        tree[base] = new_node()
    node = tree[base]
    
    # Traverse the tree according to the path segments.
    for segment in segments:
        if segment not in node["children"]:
            node["children"][segment] = new_node()
        node = node["children"][segment]
    
    # At the final node (leaf), add the full URL.
    node["urls"].append(url)

# Process every URL in the set.
for url in url_set:
    add_url_to_tree(url)

# Helper function to pretty-print the tree along with stored URLs.
def print_tree(node, path="", indent=0):
    prefix = "    " * indent
    # If there are URLs at this node, print the path and URLs.
    if node["urls"]:
        print(f"{prefix}{path} --> {node['urls']}")
    # Recursively print each child node.
    for segment, child in node["children"].items():
        # Build the full path segment.
        child_path = f"{path}/{segment}" if path else segment
        print_tree(child, child_path, indent + 1)

# Print the tree for each base domain.
for base, node in tree.items():
    print(base)
    print_tree(node, "", indent=1)
