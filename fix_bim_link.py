import re

with open('architecture.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the img src inside the bimmodeling.html link
pattern = re.compile(r'(<a href="bimmodeling\.html"[\s\S]*?<img src=")([^"]+)(")')
content = pattern.sub(r'\g<1>images/ARCHITECTURE/BIM%20Modeling/bim%20modeling%20001_01.jpg\g<3>', content)

with open('architecture.html', 'w', encoding='utf-8') as f:
    f.write(content)
