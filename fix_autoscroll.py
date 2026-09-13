import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

touch_addition = """
        scrollContainer.addEventListener('mouseleave', () => {
            isHovering = false;
            requestAnimationFrame(autoScrollStep); // resume auto scroll
            scrollContainer.classList.remove('is-scrolling');
            isScrolling = false;
            cancelAnimationFrame(scrollRAF);
            scrollSpeed = 0;
        });

        scrollContainer.addEventListener('touchstart', () => {
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
        }, { passive: true });
"""

content = content.replace("""        scrollContainer.addEventListener('mouseleave', () => {
            isHovering = false;
            requestAnimationFrame(autoScrollStep); // resume auto scroll
            scrollContainer.classList.remove('is-scrolling');
            isScrolling = false;
            cancelAnimationFrame(scrollRAF);
            scrollSpeed = 0;
        });""", touch_addition)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
