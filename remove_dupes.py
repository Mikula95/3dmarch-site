import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# find and remove the exact blocking block
to_remove = """        window.addEventListener('touchmove', function(e) {
            e.preventDefault(); // Completely block native scrolling!
        }, { passive: false });"""

content = content.replace(to_remove, "")

# also remove the duplicate touchend block which is right after it
to_remove_end = """        window.addEventListener('touchend', function(e) {
            if (isSnapping) return;
            touchEndY = e.changedTouches[0].screenY;
            const diff = touchStartY - touchEndY;
            
            if (diff > 40) {
                goToSection(currentSectionIndex + 1);
            } else if (diff < -40) {
                goToSection(currentSectionIndex - 1);
            }
        });"""

content = content.replace(to_remove_end, "")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
