import os
import re

file_to_active = {
    'index.html': 'HOMEPAGE',
    
    'architecture.html': 'Architecture',
    'archviz.html': 'Architecture',
    'archexteriors.html': 'Architecture',
    'archinteriors.html': 'Architecture',
    'conceptualdesign.html': 'Architecture',
    'revitdrafting.html': 'Architecture',
    'bimmodeling.html': 'Architecture',
    
    'productvisualization.html': 'Product Visualization',
    'furniture.html': 'Product Visualization',
    'fixtures.html': 'Product Visualization',
    'variousproductvizualisation.html': 'Product Visualization',
    
    'virtualrealms.html': 'Virtual Realms',
    'unrealengine.html': 'Virtual Realms',
    'unity.html': 'Virtual Realms',
    
    'droneservices.html': 'Drone Services',
    'droneimaging.html': 'Drone Services',
    'photogrammetry.html': 'Drone Services',
    'videomaterial.html': 'Drone Services',
    
    'blog.html': '',
}

def generate_nav(active_name):
    def active(name):
        return ' class="active"' if active_name == name else ''
        
    html = '            <ul class="nav-links" id="nav-links">\\n'
    html += f'                <li><a href="index.html"{active("HOMEPAGE")}>HOMEPAGE</a></li>\\n'
    html += f'                <li><a href="architecture.html"{active("Architecture")}>Architecture</a></li>\\n'
    html += f'                <li><a href="productvisualization.html"{active("Product Visualization")}>Product Visualization</a></li>\\n'
    html += f'                <li><a href="virtualrealms.html"{active("Virtual Realms")}>Virtual Realms</a></li>\\n'
    html += f'                <li><a href="droneservices.html"{active("Drone Services")}>Drone Services</a></li>\\n'
    html += '            </ul>'
    return html

for f in os.listdir('.'):
    if f.endswith('.html'):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        active_name = file_to_active.get(f, '')
        new_nav = generate_nav(active_name)
        
        pattern = re.compile(r'\s*<ul class="nav-links" id="nav-links">[\s\S]*?</ul>')
        content = pattern.sub('\\n' + new_nav, content)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated nav in {f}")

