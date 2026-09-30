import os
import re
import shutil
import urllib.parse

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

ordered_htmls = [
    'archexteriors.html', 'archinteriors.html', 'conceptualdesign.html', 'revitdrafting.html', 'bimmodeling.html',
    'furniture.html', 'fixtures.html', 'variousproductvizualisation.html',
    'unrealengine.html', 'unity.html',
    'droneimaging.html', 'photogrammetry.html', 'videomaterial.html',
    'archviz.html',
    'architecture.html', 'productvisualization.html', 'virtualrealms.html', 'droneservices.html',
    'index.html'
]

current_images = {}
images_dir = os.path.abspath('images')
for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif')):
            if file not in current_images:
                current_images[file] = os.path.join(root, file)

# Remove \s from excluded chars
img_regex = re.compile(r'images/([^"\'\)]+)')

image_targets = {}
for html_file in ordered_htmls:
    if not os.path.exists(html_file): continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = img_regex.findall(content)
        for match in matches:
            actual_rel_path = urllib.parse.unquote(match)
            if '?' in actual_rel_path: actual_rel_path = actual_rel_path.split('?')[0]
            filename = os.path.basename(actual_rel_path)
            if filename.lower() == 'logo.png': continue
            
            if filename not in image_targets:
                image_targets[filename] = target_folders[html_file]

replacement_map = {}

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
        
        target_rel_url = target_rel_folder.replace('\\', '/')
        new_url = f"images/{target_rel_url}/{urllib.parse.quote(filename)}"
        replacement_map[filename] = new_url

html_css_files = [f for f in os.listdir('.') if f.endswith('.html') or f == 'style.css']

for f in html_css_files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
        
        def replacer(match):
            full_match = match.group(0)
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

print("Done moving images to deep folders and updating HTML/CSS (fixed regex)!")
