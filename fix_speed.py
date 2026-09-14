import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("const duration = 250;", "const duration = 120;")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
