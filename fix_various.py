import re

with open('variousproductvizualisation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the hero-imagetop section
pattern = re.compile(r'<!-- Hero Image Top -->\s*<section class="hero-imagetop">.*?</section>', re.DOTALL)
content = pattern.sub('', content)

with open('variousproductvizualisation.html', 'w', encoding='utf-8') as f:
    f.write(content)
