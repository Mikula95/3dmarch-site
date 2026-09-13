import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'// ----- Full Page Snap Scrolling -----.*?(?=(// ----- Scroll Animations))', re.DOTALL)

new_block = """// ----- Full Page Snap Scrolling (Strict Mode) -----
    const snapSections = Array.from(document.querySelectorAll('.snap-section'));
    let isSnapping = false;
    let currentSectionIndex = 0;

    if (snapSections.length > 0) {
        
        // Hide scrollbar and disable native scrolling
        document.body.style.overflow = 'hidden';
        
        // Create Sidebar Indicators
        const indicatorContainer = document.createElement('div');
        indicatorContainer.className = 'section-indicators';
        snapSections.forEach((sec, idx) => {
            const dot = document.createElement('div');
            dot.className = 'indicator-dot';
            if (idx === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSection(idx));
            indicatorContainer.appendChild(dot);
        });
        document.body.appendChild(indicatorContainer);

        function updateIndicators(index) {
            const dots = document.querySelectorAll('.indicator-dot');
            dots.forEach((dot, idx) => {
                if (idx === index) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }

        function goToSection(index) {
            if (isSnapping || index < 0 || index >= snapSections.length || index === currentSectionIndex) return;
            isSnapping = true;
            
            const startScroll = window.scrollY;
            const targetPosition = snapSections[index].getBoundingClientRect().top + startScroll;
            const distance = targetPosition - startScroll;
            const duration = 500; 
            let start = null;
            
            currentSectionIndex = index;
            updateIndicators(index);

            function subtleEase(t, b, c, d) {
                t /= d/2;
                if (t < 1) return c/2*t*t + b;
                t--;
                return -c/2 * (t*(t-2) - 1) + b;
            }

            function animation(currentTime) {
                if (start === null) start = currentTime;
                const timeElapsed = currentTime - start;
                const run = subtleEase(timeElapsed, startScroll, distance, duration);
                
                window.scrollTo(0, run);
                
                if (timeElapsed < duration) {
                    requestAnimationFrame(animation);
                } else {
                    window.scrollTo(0, targetPosition);
                    isSnapping = false;
                }
            }
            requestAnimationFrame(animation);
        }

        window.addEventListener('wheel', function (e) {
            e.preventDefault();
            if (isSnapping) return;
            
            if (e.deltaY > 30) {
                goToSection(currentSectionIndex + 1);
            } else if (e.deltaY < -30) {
                goToSection(currentSectionIndex - 1);
            }
        }, { passive: false });

        let touchStartY = 0;
        let touchEndY = 0;
        
        window.addEventListener('touchstart', function(e) {
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: false });

        window.addEventListener('touchmove', function(e) {
            e.preventDefault(); // Completely block native scrolling!
        }, { passive: false });

        window.addEventListener('touchend', function(e) {
            if (isSnapping) return;
            touchEndY = e.changedTouches[0].screenY;
            const diff = touchStartY - touchEndY;
            
            if (diff > 40) {
                goToSection(currentSectionIndex + 1);
            } else if (diff < -40) {
                goToSection(currentSectionIndex - 1);
            }
        });
        
        // Handle window resize to realign
        window.addEventListener('resize', function() {
            if (!isSnapping) {
                window.scrollTo(0, snapSections[currentSectionIndex].getBoundingClientRect().top + window.scrollY);
            }
        });
    }

    """

new_content = pattern.sub(new_block, content)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
