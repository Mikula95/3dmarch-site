import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Make team-member a flex column
old_member = """.team-member {
    text-align: center;
    max-width: 300px;
}"""

new_member = """.team-member {
    text-align: center;
    max-width: 300px;
    display: flex;
    flex-direction: column;
}"""

content = content.replace(old_member, new_member)

# Push the button to the bottom
old_btn = """.team-member .member-btn {
    margin-top: 0.5em;
}"""

new_btn = """.team-member .member-btn {
    margin-top: auto;
}"""

content = content.replace(old_btn, new_btn)

# Change mobile align-items back to stretch
old_mobile_grid = """    .team-grid {
        flex-direction: row;
        flex-wrap: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        justify-content: flex-start;
        align-items: flex-start;
        width: 100%;"""

new_mobile_grid = """    .team-grid {
        flex-direction: row;
        flex-wrap: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        justify-content: flex-start;
        align-items: stretch;
        width: 100%;"""

content = content.replace(old_mobile_grid, new_mobile_grid)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)
