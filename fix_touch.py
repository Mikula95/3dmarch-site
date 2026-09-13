import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

touch_block = """
        let touchStartX = 0;
        let touchStartY = 0;
        let touchIsHorizontal = null;
        
        window.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
            touchIsHorizontal = null;
        }, { passive: false });

        window.addEventListener('touchmove', function(e) {
            if (isSnapping) {
                e.preventDefault();
                return;
            }
            
            if (touchIsHorizontal === null) {
                const diffX = Math.abs(e.changedTouches[0].screenX - touchStartX);
                const diffY = Math.abs(e.changedTouches[0].screenY - touchStartY);
                if (diffX > diffY) {
                    touchIsHorizontal = true;
                } else {
                    touchIsHorizontal = false;
                }
            }
            
            if (touchIsHorizontal) {
                // allow horizontal native scroll
                return;
            } else {
                // prevent vertical native scroll for fullpage
                e.preventDefault();
            }
        }, { passive: false });

        window.addEventListener('touchend', function(e) {
            if (isSnapping || touchIsHorizontal) return;
            const touchEndY = e.changedTouches[0].screenY;
            const diff = touchStartY - touchEndY;
            
            if (diff > 40) {
                goToSection(currentSectionIndex + 1);
            } else if (diff < -40) {
                goToSection(currentSectionIndex - 1);
            }
        });
"""

# replace the old touch listeners block
pattern = re.compile(r'let touchStartY = 0;.*?}\);', re.DOTALL)
new_content = pattern.sub(touch_block.strip(), content)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
