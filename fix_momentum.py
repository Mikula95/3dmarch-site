import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_touch = """        scrollContainer.addEventListener('touchstart', () => {
            isHovering = true;
            scrollContainer.classList.remove('is-scrolling');
            isScrolling = false;
            cancelAnimationFrame(scrollRAF);
            scrollSpeed = 0;
        }, { passive: true });

        scrollContainer.addEventListener('touchend', () => {
            if (isHovering) {
                isHovering = false;
                requestAnimationFrame(autoScrollStep);
            }
        }, { passive: true });"""

new_touch = """        let autoScrollTimeout = null;

        scrollContainer.addEventListener('touchstart', () => {
            isHovering = true;
            scrollContainer.classList.remove('is-scrolling');
            isScrolling = false;
            cancelAnimationFrame(scrollRAF);
            scrollSpeed = 0;
            if (autoScrollTimeout) clearTimeout(autoScrollTimeout);
        }, { passive: true });

        scrollContainer.addEventListener('touchend', () => {
            if (autoScrollTimeout) clearTimeout(autoScrollTimeout);
            autoScrollTimeout = setTimeout(() => {
                isHovering = false;
                requestAnimationFrame(autoScrollStep);
            }, 3000); // Wait 3s before resuming to allow momentum scroll
        }, { passive: true });"""

content = content.replace(old_touch, new_touch)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
