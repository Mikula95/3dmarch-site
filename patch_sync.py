import sys
import os

content = open('sync_dna.py', 'r').read()

old_logic = """        # find thumbnail (prefer w1000, then hero, then first)
        thumb_img = ""
        for img in sf_images:
            if img.startswith('w1000-'):
                thumb_img = img
                break
        if not thumb_img:
            for img in sf_images:
                if 'hero' in img.lower():
                    thumb_img = img
                    break
        if not thumb_img and sf_images:
            thumb_img = sf_images[0]
            
        img_url = f"images/{rel_folder.replace(os.sep, '/')}/{sf}/{urllib.parse.quote(thumb_img)}" if thumb_img else "" """

new_logic = """        # 1. Check parent folder (images) for "{sf} thumb.*" or similar
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
            img_url = "" """

content = content.replace(old_logic.strip(), new_logic.strip())
open('sync_dna.py', 'w').write(content)
print("Updated successfully")
