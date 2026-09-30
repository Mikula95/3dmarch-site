import os
import re
import urllib.parse
import shutil

BASE_DIR = 'images'
ROOT_DIR = '.'

def to_html_name(name):
    # E.g. "Drafting & Detailing" -> "drafting&detailing.html"
    return name.lower().replace(" ", "") + ".html"

def find_hero_img(files):
    for f in files:
        if 'hero' in f.lower() and 'mobile' not in f.lower():
            return f
    return None

def find_hero_mobile_img(files):
    for f in files:
        if 'hero' in f.lower() and 'mobile' in f.lower():
            return f
    return None

def get_images(folder_path):
    files = []
    for f in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif')):
            files.append(f)
    return files

def get_subfolders(folder_path):
    subfolders = []
    for d in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, d)):
            subfolders.append(d)
    return subfolders

def create_from_template(html_file, is_category):
    template = 'architecture.html' if is_category else 'bimmodeling.html'
    if not os.path.exists(template):
        print(f"Warning: template {template} missing.")
        return
    shutil.copy(template, html_file)
    print(f"Created {html_file} from template {template}")

def update_hero_images(html_file, rel_folder, hero_img, hero_mobile_img):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    hero_regex = re.compile(r'(<div class="hero-bg"[^>]*background-image:\s*url\()([^\)]+)(\)[^>]*>)')
    if hero_img:
        hero_url = f"images/{rel_folder.replace(os.sep, '/')}/{urllib.parse.quote(hero_img)}"
        content = hero_regex.sub(rf"\g<1>'{hero_url}'\g<3>", content)
    else:
        content = hero_regex.sub(rf"\g<1>''\g<3>", content)

    hero_mob_regex = re.compile(r'(<div class="hero-bg-mobile"[^>]*background-image:\s*url\()([^\)]+)(\)[^>]*>)')
    if hero_mobile_img:
        hero_mob_url = f"images/{rel_folder.replace(os.sep, '/')}/{urllib.parse.quote(hero_mobile_img)}"
        content = hero_mob_regex.sub(rf"\g<1>'{hero_mob_url}'\g<3>", content)
    else:
        content = hero_mob_regex.sub(rf"\g<1>''\g<3>", content)
        
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

def process_gallery(html_file, rel_folder, images):
    hero_img = find_hero_img(images)
    hero_mobile_img = find_hero_mobile_img(images)
    
    update_hero_images(html_file, rel_folder, hero_img, hero_mobile_img)
    
    gallery_files = [f for f in images if 'hero' not in f.lower()]
    thumbnails = {}
    for f in gallery_files:
        if f.startswith('w1000-'):
            orig = f[6:]
            if orig in gallery_files:
                thumbnails[orig] = f
            else:
                thumbnails[f] = f
                
    originals = []
    for f in gallery_files:
        if not f.startswith('w1000-') or (f.startswith('w1000-') and f not in thumbnails.values()):
            originals.append(f)
            
    figures = []
    for orig in originals:
        thumb = thumbnails.get(orig, orig)
        orig_url = f"images/{rel_folder.replace(os.sep, '/')}/{urllib.parse.quote(orig)}"
        thumb_url = f"images/{rel_folder.replace(os.sep, '/')}/{urllib.parse.quote(thumb)}"
        figures.append(f'                <figure class="gallery-fig zoom-in"><img src="{thumb_url}" alt="Gallery Image" data-full="{orig_url}"></figure>')
        
    gallery_html = "\\n" + "\\n".join(figures) + "\\n            "
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    gallery_regex = re.compile(r'(<div class="gallery-dynamic">)[\s\S]*?(</div>)')
    if '<div class="gallery-dynamic">' in content:
        content = gallery_regex.sub(rf'\g<1>{gallery_html}\g<2>', content)
        
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

def process_category(html_file, rel_folder, subfolders, images):
    hero_img = find_hero_img(images)
    hero_mobile_img = find_hero_mobile_img(images)
    
    update_hero_images(html_file, rel_folder, hero_img, hero_mobile_img)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    grid_regex = re.compile(r'(<div class="linkpage-grid">)[\s\S]*?(</section>)')
    match = grid_regex.search(content)
    
    descriptions = {}
    if match:
        grid_content = match.group(0)
        items = re.findall(r'<a href="([^"]+)".*?<h3>(.*?)</h3>(?:.*?<p>(.*?)</p>)?', grid_content, re.DOTALL)
        for href, title, desc in items:
            descriptions[href] = desc.strip() if desc else ""
            
    links_html = []
    for sf in subfolders:
        sf_html = to_html_name(sf)
        sf_path = os.path.join(BASE_DIR, rel_folder, sf)
        sf_images = get_images(sf_path)
        
        # 1. Check parent folder (images) for "{sf} thumb.*" or similar
        thumb_img_parent = None
        for img in images:
            if sf.lower() in img.lower() and "thumb" in img.lower():
                thumb_img_parent = img
                break
                
        # 2. Check inside sf for any image with 'thumb'
        thumb_img_sf = None
        for img in sf_images:
            if 'thumb' in img.lower():
                thumb_img_sf = img
                break
                
        # 3. Fallback to any image inside sf
        thumb_img_fallback = ""
        if sf_images:
            for img in sf_images:
                if img.startswith('w1000-'):
                    thumb_img_fallback = img
                    break
            if not thumb_img_fallback:
                thumb_img_fallback = sf_images[0]
                
        # Resolve the URL
        if thumb_img_parent:
            img_url = f"images/{rel_folder.replace(os.sep, '/')}/{urllib.parse.quote(thumb_img_parent)}"
        elif thumb_img_sf:
            img_url = f"images/{rel_folder.replace(os.sep, '/')}/{sf}/{urllib.parse.quote(thumb_img_sf)}"
        elif thumb_img_fallback:
            img_url = f"images/{rel_folder.replace(os.sep, '/')}/{sf}/{urllib.parse.quote(thumb_img_fallback)}"
        else:
            img_url = ""
            
        desc = descriptions.get(sf_html, "")
        
        link_str = f'''                <a href="{sf_html}" class="linkpage-item zoom-in">
                    <div class="item-image">
                        <img src="{img_url}" alt="{sf}">
                    </div>
                    <div class="item-caption">
                        <h3>{sf}</h3>'''
        if desc:
            link_str += f'\\n                        <p>{desc}</p>'
        link_str += '\\n                    </div>\\n                </a>'
        links_html.append(link_str)
        
    grid_inner = "\\n" + "\\n".join(links_html) + "\\n            </div>\\n        "
    
    if match:
        content = grid_regex.sub(rf'\g<1>{grid_inner}\g<2>', content)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

def sync():
    top_folders = get_subfolders(BASE_DIR)
    for folder in top_folders:
        if folder in ['INDEX', 'BLOG', 'logo']:
            continue
            
        html_file = to_html_name(folder)
        folder_path = os.path.join(BASE_DIR, folder)
        
        walk_and_sync(folder_path, folder, html_file)
        
def walk_and_sync(folder_path, rel_folder, html_file):
    subfolders = get_subfolders(folder_path)
    images = get_images(folder_path)
    
    is_category = len(subfolders) > 0
    
    if not os.path.exists(html_file):
        create_from_template(html_file, is_category)
        
    if is_category:
        process_category(html_file, rel_folder, subfolders, images)
        for sf in subfolders:
            sf_html = to_html_name(sf)
            sf_path = os.path.join(folder_path, sf)
            walk_and_sync(sf_path, os.path.join(rel_folder, sf), sf_html)
    else:
        process_gallery(html_file, rel_folder, images)

if __name__ == '__main__':
    sync()
    print("DNA Sync complete.")
