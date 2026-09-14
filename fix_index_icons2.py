import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """        let icons = [];
        const circleIcon = '<svg viewBox="0 0 24 24" fill="currentColor" width="12" height="12"><circle cx="12" cy="12" r="6"/></svg>';
        
        // Check if we are on the index page
        const isIndex = window.location.pathname === '/' || window.location.pathname.toLowerCase().endsWith('index.html');
        
        if (isIndex) {
            icons = [
                '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>',
                '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>',
                '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>',
                '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>'
            ];
        } else {
            // For all other pages, make all icons circles (or at least the first one)
            // The user asked specifically for the first section to be a circle,
            // but for generic inner pages, all sections should just be circles.
            for (let i = 0; i < snapSections.length; i++) {
                icons.push(circleIcon);
            }
        }"""

new_logic = """        let icons = [];
        const circleIcon = '<svg viewBox="0 0 24 24" fill="currentColor" width="12" height="12"><circle cx="12" cy="12" r="6"/></svg>';
        const listIcon = '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>';
        
        // Check if we are on the index page
        const isIndex = window.location.pathname === '/' || window.location.pathname.toLowerCase().endsWith('index.html');
        
        if (isIndex) {
            icons = [
                '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>', // Home
                listIcon, // 3 lines
                '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>', // Person
                '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>' // Envelope
            ];
        } else {
            // For all other pages: First icon is circle, second is list/dashes
            icons = [
                circleIcon,
                listIcon
            ];
            // If there are more than 2 sections, fallback to circles for the rest just in case
            for (let i = 2; i < snapSections.length; i++) {
                icons.push(circleIcon);
            }
        }"""

content = content.replace(old_logic, new_logic)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
