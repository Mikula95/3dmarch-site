import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("}, 50);", "}, 10);")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
