import os
import re
import shutil
import urllib.parse
from pathlib import Path

# Mapping of HTML file to target folder
target_folders = {
    'index.html': 'INDEX',
    'architecture.html': 'ARCHITECTURE',
    'archviz.html': 'ARCHITECTURE/Archviz',
    'archexteriors.html': 'ARCHITECTURE/Archviz/Arch Exteriors',
    'archinteriors.html': 'ARCHITECTURE/Archviz/Arch Interiors',
    'conceptualdesign.html': 'ARCHITECTURE/Conceptual design',
    'revitdrafting.html': 'ARCHITECTURE/Drafting & Detailing',
    'bimmodeling.html': 'ARCHITECTURE/BIM Modeling',
    'productvisualization.html': 'PRODUCT VISUALIZATION',
    'furniture.html': 'PRODUCT VISUALIZATION/FURNITURE',
    'fixtures.html': 'PRODUCT VISUALIZATION/FIXTURES',
    'variousproductvizualisation.html': 'PRODUCT VISUALIZATION/VARIOUS',
    'virtualrealms.html': 'VIRTUAL REALMS',
    'unrealengine.html': 'VIRTUAL REALMS/UNREAL ENGINE',
    'unity.html': 'VIRTUAL REALMS/UNITY',
    'droneservices.html': 'DRONE SERVICES',
    'droneimaging.html': 'DRONE SERVICES/Drone Imaging',
    'photogrammetry.html': 'DRONE SERVICES/Photogrammetry & Gaussian Splatting',
    'videomaterial.html': 'DRONE SERVICES/Video Material'
}

# Order HTML files so deeper ones claim images first
ordered_htmls = [
    'archexteriors.html', 'archinteriors.html', 'conceptualdesign.html', 'revitdrafting.html', 'bimmodeling.html',
    'furniture.html', 'fixtures.html', 'variousproductvizualisation.html',
    'unrealengine.html', 'unity.html',
    'droneimaging.html', 'photogrammetry.html', 'videomaterial.html',
    'archviz.html',
    'architecture.html', 'productvisualization.html', 'virtualrealms.html', 'droneservices.html',
    'index.html'
]

# 1. Build a map of filename -> current absolute path
current_images = {}
images_dir = os.path.abspath('images')
for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif')):
            # If there are duplicates, the first one found is kept.
            if file not in current_images:
                current_images[file] = os.path.join(root, file)

# Regex to find images in HTML/CSS
img_regex = re.compile(r'images/([^"\'\)\s]+)')

# 2. Determine target folder for each filename
image_targets = {}
for html_file in ordered_htmls:
    if not os.path.exists(html_file): continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = img_regex.findall(content)
        for match in matches:
            # Decode URL
            actual_rel_path = urllib.parse.unquote(match)
            if '?' in actual_rel_path: actual_rel_path = actual_rel_path.split('?')[0]
            filename = os.path.basename(actual_rel_path)
            
            if filename.lower() == 'logo.png': continue
            
            if filename not in image_targets:
                image_targets[filename] = target_folders[html_file]

# 3. Move files and build replacement map
replacement_map = {} # old filename (url encoded or not) -> new url path

for filename, target_rel_folder in image_targets.items():
    if filename in current_images:
        current_full_path = current_images[filename]
        new_target_dir = os.path.join(images_dir, os.path.normpath(target_rel_folder))
        os.makedirs(new_target_dir, exist_ok=True)
        new_full_path = os.path.join(new_target_dir, filename)
        
        if os.path.abspath(current_full_path) != os.path.abspath(new_full_path):
            try:
                shutil.move(current_full_path, new_full_path)
            except Exception as e:
                print(f"Error moving {filename}: {e}")
        
        # New URL path
        # Convert backslashes to forward slashes for URLs
        target_rel_url = target_rel_folder.replace('\\', '/')
        new_url = f"images/{target_rel_url}/{urllib.parse.quote(filename)}"
        replacement_map[filename] = new_url

# 4. Update all HTML and CSS files
html_css_files = [f for f in os.listdir('.') if f.endswith('.html') or f == 'style.css']

for f in html_css_files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
        
        # We need to replace ANY instance of images/.../filename with the new URL
        # We will use a regex substitution
        def replacer(match):
            full_match = match.group(0) # e.g. images/ARCHEXTERIORS/foo.jpg
            rel_path = urllib.parse.unquote(match.group(1))
            if '?' in rel_path: rel_path = rel_path.split('?')[0]
            filename = os.path.basename(rel_path)
            if filename in replacement_map:
                return replacement_map[filename]
            return full_match
            
        content = img_regex.sub(replacer, content)
        
        if content != original_content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {f}")

print("Done moving images to deep folders and updating HTML/CSS!")
