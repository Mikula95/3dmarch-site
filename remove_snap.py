import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("scroll-snap-type: x mandatory;", "")
content = content.replace("scroll-snap-align: center;", "")

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)
