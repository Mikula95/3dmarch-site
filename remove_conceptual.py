import re

with open('architecture.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'\s*<a href="conceptualdesign\.html" class="linkpage-item zoom-in">[\s\S]*?</a>')
content = pattern.sub('', content)

with open('architecture.html', 'w', encoding='utf-8') as f:
    f.write(content)
