import re
from pathlib import Path

# Return true or false if the link from the page is valid
def resolve(page, link):
    # Test whether the relative path leads to something real
    if page.parent.joinpath(link).exists():
        return True
    # We failed to resolve the link, so check if it's an https path
    else:
        link_name = "[^\[]+"
        link_url = "http[s]?://.+"
        markup_regex = f'\[({link_name})]\(\s*({link_url})\s*\)'
        for match in re.findall(markup_regex, '[a link](' + link + ')'):
            # Link resolved
            #print("[INFO] Resolved link[", link, "] in page[", page, "]")
            return True
        header_result = re.compile(r'#').findall(link)
        if (len(header_result) > 0):
            #print("Header link [", link, "] in page[", page, "]")
            return True
    # If we've made it this far, verification failed
    print("Failed to resolve link[", link, "] in page[", page, "]")
    return False

parent = Path(__file__).resolve().parent
print("root:", parent)

# First, get a list of all markdown files
md_pages = []
for p in parent.rglob("*.md"):
    md_pages.append(p)
print("Detected", len(md_pages), "pages")

# Second, for each markdown file, grab a link and pair it
# to the main page's link.
INLINE_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
links_detected = 0
links_verified = 0
links_verified = 0
for page in md_pages:
    try:
        # Attempt to extract all of the links in the page
        result = INLINE_LINK_RE.findall(page.read_text())
        for match in result:
            link = match[1]
            links_detected += 1
            if resolve(page, link):
                links_verified += 1
    except:
        print("[ERROR] Failed to parse text on page", page)
print("Detected", links_detected, "links")
print(links_verified, "/", links_detected, "verified")

todos = 0
for page in md_pages:
    try:
        # Attempt to count total number of TODOs left
        result = re.compile(r'TODO').findall(page.read_text())
        todos += len(result)
    except:
        print("[ERROR] Failed to parse text on page", page)
print(todos, "TODOs remaining")



