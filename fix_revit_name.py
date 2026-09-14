import os

files_to_update = ['architecture.html', 'revitdrafting.html']

for file in files_to_update:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = content.replace("Revit Drafting & Detailing", "Drafting & Detailing")
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
