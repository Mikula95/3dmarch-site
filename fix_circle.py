import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_svg = '<svg viewBox="0 0 24 24" fill="currentColor" width="12" height="12"><circle cx="12" cy="12" r="6"/></svg>'
new_svg = '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><circle cx="12" cy="12" r="8"/></svg>'

content = content.replace(old_svg, new_svg)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
