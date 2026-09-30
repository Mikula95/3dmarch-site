import os, re
html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if r"\'" in content:
        content = content.replace(r"\'", "'")
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed quotes in {f}")
