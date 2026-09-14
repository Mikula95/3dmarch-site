import re

with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the portraits smaller on desktop
content = re.sub(r'\.team-member \.member-img \{\s*width: 240px;\s*height: 240px;', r'.team-member .member-img {\n    width: 160px;\n    height: 160px;', content)

# Remove the huge bouncy animation and make it like linkpage-item
# Old hover animation:
old_anim = """.team-member:hover .member-img {
    transform: translateY(-15px) scale(1.15);
    box-shadow: 0 30px 50px rgba(0,0,0,0.9), 0 0 25px rgba(255,255,255,0.2);
    border-color: rgba(255, 255, 255, 0.6);
}"""

new_anim = """.team-member:hover .member-img {
    filter: saturate(100%) brightness(1.1);
    transform: scale(1.08);
}"""

content = content.replace(old_anim, new_anim)

# Remove the text bouncy animation too, just in case that's annoying
old_text_anim = """.team-member:hover .member-name {
    transform: translateY(-5px) scale(1.05);
    color: #fff;
    text-shadow: 0 0 15px rgba(255,255,255,0.6);
}"""

new_text_anim = """.team-member:hover .member-name {
    color: var(--hover-color);
}"""

content = content.replace(old_text_anim, new_text_anim)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)
