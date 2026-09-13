import os

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the block starting at "// ----- Full Page Snap Scrolling -----"
# up to "// ----- Scroll Animations (IntersectionObserver) -----"

import re
pattern = re.compile(r'// ----- Full Page Snap Scrolling -----.*?(?=(// ----- Scroll Animations))', re.DOTALL)

new_block = """// ----- Full Page Snap Scrolling -----
    const snapSections = Array.from(document.querySelectorAll('.snap-section'));
    let isSnapping = false;

    if (snapSections.length > 0) {
        function handleSnap(direction) {
            const scrollPos = window.scrollY;
            const threshold = 50; 
            
            let currentIndex = -1;
            for (let i = 0; i < snapSections.length; i++) {
                const rect = snapSections[i].getBoundingClientRect();
                if (Math.abs(rect.top) < threshold) {
                    currentIndex = i;
                    break;
                }
            }

            if (currentIndex !== -1) {
                let targetIndex = -1;

                if (direction > 0 && currentIndex < snapSections.length - 1) {
                    targetIndex = currentIndex + 1;
                } else if (direction < 0 && currentIndex > 0) {
                    targetIndex = currentIndex - 1;
                }

                if (targetIndex !== -1) {
                    isSnapping = true;
                    document.documentElement.style.scrollBehavior = 'auto';
                    
                    const targetPosition = snapSections[targetIndex].getBoundingClientRect().top + scrollPos;
                    const distance = targetPosition - scrollPos;
                    const duration = 300; 
                    let start = null;

                    function subtleEase(t, b, c, d) {
                        t /= d/2;
                        if (t < 1) return c/2*t*t + b;
                        t--;
                        return -c/2 * (t*(t-2) - 1) + b;
                    }

                    function animation(currentTime) {
                        if (start === null) start = currentTime;
                        const timeElapsed = currentTime - start;
                        const run = subtleEase(timeElapsed, scrollPos, distance, duration);
                        
                        window.scrollTo(0, run);
                        
                        if (timeElapsed < duration) {
                            requestAnimationFrame(animation);
                        } else {
                            window.scrollTo(0, targetPosition);
                            document.documentElement.style.scrollBehavior = '';
                            isSnapping = false;
                        }
                    }
                    requestAnimationFrame(animation);
                    return true;
                }
            }
            return false;
        }

        window.addEventListener('wheel', function (e) {
            if (isSnapping) { e.preventDefault(); return; }
            if (handleSnap(e.deltaY > 0 ? 1 : -1)) {
                e.preventDefault();
            }
        }, { passive: false });

        let touchStartY = 0;
        let touchEndY = 0;
        
        window.addEventListener('touchstart', function(e) {
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: false });

        window.addEventListener('touchmove', function(e) {
            if (isSnapping) {
                e.preventDefault();
            }
        }, { passive: false });

        window.addEventListener('touchend', function(e) {
            if (isSnapping) return;
            touchEndY = e.changedTouches[0].screenY;
            const diff = touchStartY - touchEndY;
            
            if (Math.abs(diff) > 40) {
                handleSnap(diff > 0 ? 1 : -1);
            }
        });
    }

    """

new_content = pattern.sub(new_block, content)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
