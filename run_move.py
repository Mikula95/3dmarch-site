import os
import re
import shutil
import urllib.parse

categories = {
    'INDEX': ['index.html'],
    'ARCHITECTURE': ['architecture.html', 'archviz.html', 'archexteriors.html', 'archinteriors.html', 'conceptualdesign.html', 'revitdrafting.html', 'bimmodeling.html'],
    'PRODUCT VISUALIZATION': ['productvisualization.html', 'furniture.html', 'fixtures.html', 'variousproductvizualisation.html'],
    'VIRTUAL REALMS': ['virtualrealms.html', 'unrealengine.html', 'unity.html', 'gameassets.html'],
    'DRONE SERVICES': ['droneservices.html', 'droneimaging.html', 'photogrammetry.html', 'videomaterial.html']
}

html_files = [f for f in os.listdir('.') if f.endswith('.html') or f == 'style.css']

# We want to match images/...
# Note: we need to handle URL encoded spaces. E.g. DRONE%20IMAGING
img_regex = re.compile(r'images/([^"\'\)]+)')

image_category_map = {}

for category, files in categories.items():
    for f in files:
        if os.path.exists(f):
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                matches = img_regex.findall(content)
                for match in matches:
                    if 'logo.png' in match.lower() or '3dmarch_showreel.mp4' in match.lower():
                        continue
                    
                    if match not in image_category_map:
                        image_category_map[match] = category
                    else:
                        if image_category_map[match] == 'INDEX' and category != 'INDEX':
                            image_category_map[match] = category

# Make sure all categories have physical folders
for cat in categories.keys():
    folder_path = os.path.join('images', cat)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

# Now, we will map each original match string to its new full path relative to the root (e.g., images/ARCHITECTURE/filename.jpg)
# We need to move the file physically.
replacement_map = {}
for match_str, category in image_category_map.items():
    # URL decode the string to find the actual file on disk
    actual_rel_path = urllib.parse.unquote(match_str)
    
    # In case there's query strings like ?v=1 or something (unlikely for images here, but safe)
    if '?' in actual_rel_path:
        actual_rel_path = actual_rel_path.split('?')[0]
        
    old_full_path = os.path.join('images', actual_rel_path)
    
    # We will extract just the filename so we can place it in the new category folder directly
    filename = os.path.basename(actual_rel_path)
    new_full_path = os.path.join('images', category, filename)
    
    # Note: Some files might already be in the target folder, e.g., if old path was images/ARCHITECTURE/file.jpg
    if os.path.exists(old_full_path) and os.path.abspath(old_full_path) != os.path.abspath(new_full_path):
        try:
            shutil.move(old_full_path, new_full_path)
        except Exception as e:
            print(f"Error moving {old_full_path} to {new_full_path}: {e}")
            
    # The new URL in the HTML should be URL encoded
    # e.g., images/PRODUCT VISUALIZATION/filename.jpg -> images/PRODUCT%20VISUALIZATION/filename.jpg
    # Actually, we can just replace the match string.
    # The old string was images/{match_str}
    # The new string should be images/{category}/{filename}
    
    # Let's handle urlencoding for the new string
    new_url_path = f"images/{category}/{urllib.parse.quote(filename)}"
    replacement_map[f"images/{match_str}"] = new_url_path

# Now update all HTML and CSS files
for f in html_files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # Sort replacements by length descending so we don't accidentally replace substrings
        sorted_replacements = sorted(replacement_map.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old_str, new_str in sorted_replacements:
            content = content.replace(old_str, new_str)
            
        if content != original_content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {f}")

print("Done moving images and updating files.")
