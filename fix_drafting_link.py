import re
import urllib.parse

with open('architecture.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the img src inside the revitdrafting.html link
# The path contains '&' and spaces, so it should be properly URL encoded
img_path = "images/ARCHITECTURE/Drafting & Detailing/drafting 001.png"
encoded_path = "images/ARCHITECTURE/Drafting%20%26%20Detailing/drafting%20001.png"

pattern = re.compile(r'(<a href="revitdrafting\.html"[\s\S]*?<img src=")([^"]+)(")')
content = pattern.sub(r'\g<1>' + encoded_path + r'\g<3>', content)

with open('architecture.html', 'w', encoding='utf-8') as f:
    f.write(content)
