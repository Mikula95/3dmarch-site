import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the navbar hiding logic to only target the linkpage-grid container
old_logic = """            // Hide navbar completely in "What We Do" section for pure full screen
            if (whatWeDoSection) {
                const rect = whatWeDoSection.getBoundingClientRect();
                // If What We Do section is taking up the screen, hide nav
                if (rect.top <= 50 && rect.bottom >= window.innerHeight - 50) {
                    nav.style.transform = 'translateY(-100%)';
                    nav.style.pointerEvents = 'none';
                } else {
                    nav.style.transform = '';
                    nav.style.pointerEvents = 'auto';
                }
            }"""

new_logic = """            // Hide navbar completely in "What We Do" section for pure full screen
            if (whatWeDoSection && whatWeDoSection.querySelector('.linkpage-grid')) {
                const rect = whatWeDoSection.getBoundingClientRect();
                // If What We Do section is taking up the screen, hide nav
                if (rect.top <= 50 && rect.bottom >= window.innerHeight - 50) {
                    nav.style.transform = 'translateY(-100%)';
                    nav.style.pointerEvents = 'none';
                } else {
                    nav.style.transform = '';
                    nav.style.pointerEvents = 'auto';
                }
            }"""

content = content.replace(old_logic, new_logic)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
