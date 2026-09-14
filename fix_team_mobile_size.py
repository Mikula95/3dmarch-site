import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the portraits smaller on mobile
content = re.sub(r'\.team-member \.member-img \{\s*width: 150px;\s*height: 150px;\s*\}', r'.team-member .member-img {\n        width: 100px;\n        height: 100px;\n    }', content)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)
