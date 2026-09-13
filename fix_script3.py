import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the overflow hidden line
content = content.replace("document.body.style.overflow = 'hidden';", "/* Custom scroll lock using events */")

# Add keydown prevention for scrolling
keydown_block = """
        window.addEventListener('keydown', function(e) {
            if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Space'].includes(e.code)) {
                e.preventDefault();
                if (isSnapping) return;
                if (e.code === 'ArrowDown' || e.code === 'PageDown' || e.code === 'Space') {
                    goToSection(currentSectionIndex + 1);
                } else {
                    goToSection(currentSectionIndex - 1);
                }
            }
        }, { passive: false });
"""
content = content.replace("window.addEventListener('wheel',", keydown_block + "\n        window.addEventListener('wheel',")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
