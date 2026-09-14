import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific scroll logic with a reusable function
old_scroll_logic = """    // ----- Horizontal Scroll Active Item & Edge Scroll -----
    const scrollContainer = document.querySelector('.linkpage-grid');
    const scrollItems = document.querySelectorAll('.linkpage-item');
    if (scrollContainer && scrollItems.length > 0) {


        // Edge Scrolling and Auto-Scroll
        let scrollRAF;
        let isScrolling = false;
        let scrollSpeed = 0;
        let isHovering = false;
        let autoScrollSpeed = 1.5;

        function scrollStep() {
            if (isScrolling && scrollSpeed !== 0) {
                scrollContainer.scrollBy({ left: scrollSpeed, behavior: 'auto' });
                scrollRAF = requestAnimationFrame(scrollStep);
            }
        }

        function autoScrollStep() {
            if (!isHovering) {
                scrollContainer.scrollBy({ left: autoScrollSpeed, behavior: 'auto' });
                
                // Ping-pong if hitting ends
                if (scrollContainer.scrollLeft >= (scrollContainer.scrollWidth - scrollContainer.clientWidth - 1)) {
                    autoScrollSpeed = -1.5;
                } else if (scrollContainer.scrollLeft <= 1) {
                    autoScrollSpeed = 1.5;
                }
                
                requestAnimationFrame(autoScrollStep);
            }
        }
        
        // Start auto-scroll by default
        requestAnimationFrame(autoScrollStep);

        scrollContainer.addEventListener('mouseenter', () => {
            isHovering = true;
        });

        scrollContainer.addEventListener('mousemove', (e) => {
            const rect = scrollContainer.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            
            const edgeThreshold = window.innerWidth * 0.15; // 15% of screen width from edges
            const maxSpeed = 10; 
            
            if (mouseX > rect.width - edgeThreshold) {
                // Scroll Right
                scrollContainer.classList.add('is-scrolling');
                scrollSpeed = maxSpeed;
                if (!isScrolling) {
                    isScrolling = true;
                    scrollRAF = requestAnimationFrame(scrollStep);
                }
            } else if (mouseX < edgeThreshold) {
                // Scroll Left
                scrollContainer.classList.add('is-scrolling');
                scrollSpeed = -maxSpeed;
                if (!isScrolling) {
                    isScrolling = true;
                    scrollRAF = requestAnimationFrame(scrollStep);
                }
            } else {
                scrollContainer.classList.remove('is-scrolling');
                isScrolling = false;
                cancelAnimationFrame(scrollRAF);
                scrollSpeed = 0;
            }
        });


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
            isHovering = false;
            requestAnimationFrame(autoScrollStep);
        }, { passive: true });"""

new_scroll_logic = """    // ----- Horizontal Scroll Active Item & Edge Scroll -----
    function initAutoScroll(containerSelector) {
        const scrollContainer = document.querySelector(containerSelector);
        if (!scrollContainer) return;

        let scrollRAF;
        let isScrolling = false;
        let scrollSpeed = 0;
        let isHovering = false;
        let autoScrollSpeed = 1.5;
        let autoScrollTimeout = null;

        function scrollStep() {
            if (isScrolling && scrollSpeed !== 0) {
                scrollContainer.scrollBy({ left: scrollSpeed, behavior: 'auto' });
                scrollRAF = requestAnimationFrame(scrollStep);
            }
        }

        function autoScrollStep() {
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
        }
        
        // Start auto-scroll by default
        requestAnimationFrame(autoScrollStep);

        scrollContainer.addEventListener('mouseenter', () => {
            isHovering = true;
        });

        scrollContainer.addEventListener('mousemove', (e) => {
            // Mouse panning logic only makes sense if it's scrollable
            if (scrollContainer.scrollWidth <= scrollContainer.clientWidth) return;
            
            const rect = scrollContainer.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            
            const edgeThreshold = window.innerWidth * 0.15;
            const maxSpeed = 10; 
            
            if (mouseX > rect.width - edgeThreshold) {
                scrollContainer.classList.add('is-scrolling');
                scrollSpeed = maxSpeed;
                if (!isScrolling) {
                    isScrolling = true;
                    scrollRAF = requestAnimationFrame(scrollStep);
                }
            } else if (mouseX < edgeThreshold) {
                scrollContainer.classList.add('is-scrolling');
                scrollSpeed = -maxSpeed;
                if (!isScrolling) {
                    isScrolling = true;
                    scrollRAF = requestAnimationFrame(scrollStep);
                }
            } else {
                scrollContainer.classList.remove('is-scrolling');
                isScrolling = false;
                cancelAnimationFrame(scrollRAF);
                scrollSpeed = 0;
            }
        });

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
            if (autoScrollTimeout) clearTimeout(autoScrollTimeout);
        }, { passive: true });

        scrollContainer.addEventListener('touchend', () => {
            if (autoScrollTimeout) clearTimeout(autoScrollTimeout);
            autoScrollTimeout = setTimeout(() => {
                isHovering = false;
                requestAnimationFrame(autoScrollStep);
            }, 3000); // Wait 3s before resuming to allow momentum scroll
        }, { passive: true });
    }

    initAutoScroll('.linkpage-grid');
    initAutoScroll('.team-grid');

    const scrollContainer = document.querySelector('.linkpage-grid');
    const scrollItems = document.querySelectorAll('.linkpage-item');
    if (scrollContainer && scrollItems.length > 0) {"""

# Replace old scroll logic using string replace
if old_scroll_logic in content:
    content = content.replace(old_scroll_logic, new_scroll_logic)
else:
    print("Could not find the old block. Maybe it was modified?")

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
