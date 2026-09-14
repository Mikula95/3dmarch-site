import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

old_css = """.indicator-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.4);
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.indicator-dot.active {
    background: #ffffff;
    transform: scale(1.3);
}"""

new_css = """.indicator-dot {
    width: 24px;
    height: 24px;
    background: transparent;
    cursor: pointer;
    transition: transform 0.3s ease, color 0.3s ease;
    border: none;
    color: rgba(255, 255, 255, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
}

.indicator-dot.active {
    background: transparent;
    transform: scale(1.2);
    color: #ffffff;
}"""

content = content.replace(old_css, new_css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)
