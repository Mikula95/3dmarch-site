import os
import re
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

base_dir = os.path.abspath('images')

for html_file, rel_folder in target_folders.items():
    if not os.path.exists(html_file):
        continue
        
    folder_path = os.path.join(base_dir, os.path.normpath(rel_folder))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        
    all_files = []
    for f in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif')):
            all_files.append(f)
            
    # Find hero
    hero_img = None
    for f in all_files:
        if 'hero' in f.lower() and 'mobile' not in f.lower():
            hero_img = f
            break
            
    hero_mobile_img = None
    for f in all_files:
        if 'hero' in f.lower() and 'mobile' in f.lower():
            hero_mobile_img = f
            break
            
    gallery_files = [f for f in all_files if 'hero' not in f.lower()]
    
    thumbnails = {}
    for f in gallery_files:
        if f.startswith('w1000-'):
            original = f[6:]
            if original in gallery_files:
                thumbnails[original] = f
            else:
                thumbnails[f] = f
                
    originals = []
    for f in gallery_files:
        if not f.startswith('w1000-') or (f.startswith('w1000-') and f not in thumbnails.values()):
            originals.append(f)
            
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
        
    original_content = content
    
    # 1. Update hero image
    hero_regex = re.compile(r'(<div class="hero-bg"[^>]*background-image:\s*url\()([^\)]+)(\)[^>]*>)')
    if hero_img:
        hero_url = f"images/{rel_folder.replace('\\', '/')}/{urllib.parse.quote(hero_img)}"
        content = hero_regex.sub(rf"\g<1>'{hero_url}'\g<3>", content)
    else:
        # But wait, index.html uses video! Don't touch index.html hero if it's not a div.
        # It's <video autoplay loop muted playsinline class="hero-bg hero-video">
        # My regex only matches <div class="hero-bg" ... background-image: ...> so it's safe.
        content = hero_regex.sub(rf"\g<1>''\g<3>", content)

    # 1b. Update hero mobile image
    hero_mob_regex = re.compile(r'(<div class="hero-bg-mobile"[^>]*background-image:\s*url\()([^\)]+)(\)[^>]*>)')
    if hero_mobile_img:
        hero_mob_url = f"images/{rel_folder.replace('\\', '/')}/{urllib.parse.quote(hero_mobile_img)}"
        content = hero_mob_regex.sub(rf"\g<1>'{hero_mob_url}'\g<3>", content)
    else:
        content = hero_mob_regex.sub(rf"\g<1>''\g<3>", content)

    # 2. Update gallery
    gallery_html = ""
    if html_file not in ['index.html', 'architecture.html', 'archviz.html', 'productvisualization.html', 'virtualrealms.html', 'droneservices.html']:
        if len(originals) > 0:
            figures = []
            for orig in originals:
                thumb = thumbnails.get(orig, orig)
                orig_url = f"images/{rel_folder.replace('\\', '/')}/{urllib.parse.quote(orig)}"
                thumb_url = f"images/{rel_folder.replace('\\', '/')}/{urllib.parse.quote(thumb)}"
                figures.append(f'                <figure class="gallery-fig zoom-in"><img src="{thumb_url}" alt="Gallery Image" data-full="{orig_url}"></figure>')
            gallery_html = "\\n" + "\\n".join(figures) + "\\n            "
        
        if '<div class="gallery-dynamic">' in content:
            gallery_regex = re.compile(r'(<div class="gallery-dynamic">)[\s\S]*?(</div>)')
            content = gallery_regex.sub(rf'\g<1>{gallery_html}\g<2>', content)
        
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {html_file}")

print("Sync complete.")
