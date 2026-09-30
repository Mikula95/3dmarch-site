import os
import re
import shutil

categories = {
    'INDEX': ['index.html'],
    'ARCHITECTURE': ['architecture.html', 'archviz.html', 'archexteriors.html', 'archinteriors.html', 'conceptualdesign.html', 'revitdrafting.html', 'bimmodeling.html'],
    'PRODUCT VISUALIZATION': ['productvisualization.html', 'furniture.html', 'fixtures.html', 'variousproductvizualisation.html'],
    'VIRTUAL REALMS': ['virtualrealms.html', 'unrealengine.html', 'unity.html', 'gameassets.html'],
    'DRONE SERVICES': ['droneservices.html', 'droneimaging.html', 'photogrammetry.html', 'videomaterial.html']
}

# Add all html files just in case
all_files = []
for f in os.listdir('.'):
    if f.endswith('.html') or f == 'style.css':
        all_files.append(f)

# Regex to find image references: src="images/...", url('images/...'), data-full="images/..."
# We want to match the whole path after 'images/'
img_regex = re.compile(r'images/([^"\'\)]+)')

# Map from old image path (relative to images/) to new category
image_category_map = {}

for category, files in categories.items():
    for f in files:
        if os.path.exists(f):
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                matches = img_regex.findall(content)
                for match in matches:
                    if match.lower() == 'logo.png':
                        continue # leave logo alone or maybe move to INDEX? Let's leave in root for now.
                    if '3dmarch_showreel.mp4' in match:
                        continue # leave video alone
                    if match not in image_category_map:
                        image_category_map[match] = category
                    else:
                        # If already assigned, maybe index.html is parsing. Let's prioritize sub-categories over INDEX
                        if image_category_map[match] == 'INDEX' and category != 'INDEX':
                            image_category_map[match] = category

print("Found image mappings:")
for img, cat in image_category_map.items():
    print(f"{img} -> {cat}")

