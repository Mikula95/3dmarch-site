import urllib.parse
import re

htmls = ['productvisualization.html', 'virtualrealms.html']
folders = ['PRODUCT VISUALIZATION', 'VIRTUAL REALMS']
images = ['PRODUCT VISUALIZATION hero.jpg', 'VIRTUAL REALMS HERO.png']

for i in range(2):
    with open(htmls[i], 'r', encoding='utf-8') as f:
        content = f.read()
        
    url = f"images/{folders[i]}/{urllib.parse.quote(images[i])}"
    
    # We replace url('') or url('...')
    # Let's just use string replace to be safe and forceful
    # Find background-image: url('...');
    content = re.sub(r'background-image:\s*url\([^)]+\)', f"background-image: url('{url}')", content)
    
    with open(htmls[i], 'w', encoding='utf-8') as f:
        f.write(content)
