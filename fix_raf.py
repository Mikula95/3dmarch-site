import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """    function initAutoScroll(containerSelector) {
        const scrollContainer = document.querySelector(containerSelector);
        if (!scrollContainer) return;

        let scrollRAF;
        let isScrolling = false;
        let scrollSpeed = 0;
        let isHovering = false;
        let autoScrollSpeed = 0.5;
        let autoScrollTimeout = null;"""

new_logic = """    function initAutoScroll(containerSelector) {
        const scrollContainer = document.querySelector(containerSelector);
        if (!scrollContainer) return;

        let scrollRAF;
        let isScrolling = false;
        let scrollSpeed = 0;
        let isHovering = false;
        let autoScrollSpeed = 0.5;
        let autoScrollTimeout = null;
        let autoScrollRAF = null;"""

content = content.replace(old_logic, new_logic)

old_step = """        function autoScrollStep() {
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
        }
        
        // Start auto-scroll by default
        requestAnimationFrame(autoScrollStep);"""


new_step = """        function autoScrollStep() {
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
                
                autoScrollRAF = requestAnimationFrame(autoScrollStep);
            }
        }
        
        // Start auto-scroll by default
        autoScrollRAF = requestAnimationFrame(autoScrollStep);"""

content = content.replace(old_step, new_step)

old_leave = """        scrollContainer.addEventListener('mouseleave', () => {
            isHovering = false;
            requestAnimationFrame(autoScrollStep); // resume auto scroll
            scrollContainer.classList.remove('is-scrolling');
            isScrolling = false;
            cancelAnimationFrame(scrollRAF);
            scrollSpeed = 0;
        });"""

new_leave = """        scrollContainer.addEventListener('mouseleave', () => {
            isHovering = false;
            cancelAnimationFrame(autoScrollRAF);
            autoScrollRAF = requestAnimationFrame(autoScrollStep); // resume auto scroll
            scrollContainer.classList.remove('is-scrolling');
            isScrolling = false;
            cancelAnimationFrame(scrollRAF);
            scrollSpeed = 0;
        });"""

content = content.replace(old_leave, new_leave)

old_touch = """        scrollContainer.addEventListener('touchend', () => {
            if (autoScrollTimeout) clearTimeout(autoScrollTimeout);
            autoScrollTimeout = setTimeout(() => {
                isHovering = false;
                requestAnimationFrame(autoScrollStep);
            }, 3000); // Wait 3s before resuming to allow momentum scroll
        }, { passive: true });"""

new_touch = """        scrollContainer.addEventListener('touchend', () => {
            if (autoScrollTimeout) clearTimeout(autoScrollTimeout);
            autoScrollTimeout = setTimeout(() => {
                isHovering = false;
                cancelAnimationFrame(autoScrollRAF);
                autoScrollRAF = requestAnimationFrame(autoScrollStep);
            }, 3000); // Wait 3s before resuming to allow momentum scroll
        }, { passive: true });"""

content = content.replace(old_touch, new_touch)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
