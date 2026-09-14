import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

old_not_hover = """.team-grid:hover .team-member:not(:hover) .member-img {
    filter: brightness(0.5) saturate(30%);
    transform: scale(0.9);
    box-shadow: 0 5px 10px rgba(0,0,0,0.3);
}"""

new_not_hover = """.team-grid:hover .team-member:not(:hover) .member-img {
    filter: brightness(0.4) saturate(10%);
}"""

content = content.replace(old_not_hover, new_not_hover)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)
