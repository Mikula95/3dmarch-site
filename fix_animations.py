import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Change duration = 500 to duration = 250
content = re.sub(r'const duration = 500;\s*', r'const duration = 250;\n            ', content)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)

with open('style.css', 'r', encoding='utf-8') as f:
    style_content = f.read()

# Change transition: opacity 0.8s ease, transform 0.8s ease;
style_content = re.sub(r'transition:\s*opacity\s*0\.8s\s*ease,\s*transform\s*0\.8s\s*ease;', 'transition: opacity 0.3s ease, transform 0.3s ease;', style_content)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(style_content)

