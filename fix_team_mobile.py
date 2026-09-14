import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the mobile .team-grid rule
old_css = """    .team-grid {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 1em;
        margin-top: 1em;
    }
    .team-member {
        max-width: 45%;
    }
    .team-member .member-img {
        width: 120px;
        height: 120px;
    }"""

new_css = """    .team-grid {
        flex-direction: row;
        flex-wrap: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        justify-content: flex-start;
        align-items: center;
        width: 100%;
        padding: 0 5vw;
        gap: 1.5em;
        margin-top: 2em;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none; /* Firefox */
    }
    .team-grid::-webkit-scrollbar {
        display: none; /* Chrome, Safari, Edge */
    }
    .team-member {
        flex: 0 0 60%;
        max-width: none;
        scroll-snap-align: center;
    }
    .team-member .member-img {
        width: 150px;
        height: 150px;
    }"""

content = content.replace(old_css, new_css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)
