import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """        function autoScrollStep() {
            if (!isHovering) {
                // Only scroll if it's actually horizontally scrollable
                if (scrollContainer.scrollWidth > scrollContainer.clientWidth) {
                    scrollContainer.scrollBy({ left: autoScrollSpeed, behavior: 'auto' });
                    
                    // Ping-pong if hitting ends
                    if (scrollContainer.scrollLeft >= (scrollContainer.scrollWidth - scrollContainer.clientWidth - 1)) {
                        autoScrollSpeed = -1.5;
                    } else if (scrollContainer.scrollLeft <= 1) {
                        autoScrollSpeed = 1.5;
                    }
                }
                
                requestAnimationFrame(autoScrollStep);
            }
        }"""

new_logic = """        function autoScrollStep() {
            if (!isHovering) {
                // Only scroll if it's actually horizontally scrollable by a meaningful margin
                if (scrollContainer.scrollWidth > scrollContainer.clientWidth + 20) {
                    scrollContainer.scrollBy({ left: autoScrollSpeed, behavior: 'auto' });
                    
                    // Ping-pong if hitting ends
                    // Added a larger threshold (5px) to prevent sub-pixel vibration
                    if (scrollContainer.scrollLeft >= (scrollContainer.scrollWidth - scrollContainer.clientWidth - 5)) {
                        autoScrollSpeed = -0.5; // slow down to chess piece speed
                    } else if (scrollContainer.scrollLeft <= 5) {
                        autoScrollSpeed = 0.5; // slow down to chess piece speed
                    }
                }
                
                requestAnimationFrame(autoScrollStep);
            }
        }"""

content = content.replace(old_logic, new_logic)

# Also change the default autoScrollSpeed declaration
content = content.replace("let autoScrollSpeed = 1.5;", "let autoScrollSpeed = 0.5;")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
