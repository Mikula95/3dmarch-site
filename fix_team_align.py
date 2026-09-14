import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

old_css = """    .team-grid {
        flex-direction: row;
        flex-wrap: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        justify-content: flex-start;
        align-items: center;
        width: 100%;"""

new_css = """    .team-grid {
        flex-direction: row;
        flex-wrap: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        justify-content: flex-start;
        align-items: flex-start;
        width: 100%;"""

content = content.replace(old_css, new_css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)
