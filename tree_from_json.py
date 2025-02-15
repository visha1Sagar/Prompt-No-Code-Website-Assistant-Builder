import json
from urllib.parse import urlparse


# Define a function to create a new tree node.
def new_node():
    return {"children": {}, "urls": [], "markdowns": []}

def create_tree_from_json(input_file: str = "crawl_results.json", output_file: str = "tree_output.json"):

    # Load the JSON data from a file named "data.json"
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # We'll build the tree using the base domain as the top-level key.
    tree = {}


    def add_url_to_tree(url, markdown=None):
        parsed = urlparse(url)
        # Get non-empty path segments
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

        # At the leaf node, add the full URL and, if available, its markdown.
        if url not in node["urls"]:
            node["urls"].append(url)
        if markdown:
            node["markdowns"].append(markdown)


    # Process the pages dictionary: add each key (with markdown) and its child_urls.
    pages = data.get("pages", {})
    for url, page in pages.items():
        markdown = page.get("markdown")
        add_url_to_tree(url, markdown)
        for child in page.get("child_urls", []):
            add_url_to_tree(child)

    # Also add the root URL if available (without markdown)
    if "root" in data:
        add_url_to_tree(data["root"])


    # Save the resulting tree to a JSON file.
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(tree, outfile, indent=4)

    print("Tree saved to 'tree_output.json'")



def extract_markdowns(data):
    markdowns = []

    def traverse(node):
        if isinstance(node, dict):
            if "markdowns" in node:
                markdowns.extend(node["markdowns"])
            for key in node:
                traverse(node[key])
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(data)
    return markdowns

create_tree_from_json()

# def print_tree(node, path="", indent=0):
#     prefix = "    " * indent
#     if node["urls"] or node["markdowns"]:
#         print(f"{prefix}{path} --> URLs: {node['urls']}")
#         if node["markdowns"]:
#             print(f"{prefix}         Markdown: {node['markdowns']}")
#     for segment, child in node["children"].items():
#         child_path = f"{path}/{segment}" if path else segment
#         print_tree(child, child_path, indent + 1)
#
#
#
#
# # (Optional) Print the tree for each base domain.
# for base, node in tree.items():
#     print(base)
#     print_tree(node, "", indent=1)
create_tree_from_json()