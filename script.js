/* =============================================
   3DMARCH - Script
   Hamburger menu, scroll animations, lightbox,
   modal form, blog search/filter, feather icons
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {

    // ----- Feather Icons -----
    if (typeof feather !== 'undefined') {
        feather.replace();
    }

    // ----- Hamburger Menu -----
    const hamburger = document.getElementById('hamburger-btn');
    const navLinks = document.getElementById('nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function () {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
    }

    // ----- Navbar scroll background & shrink -----
    const nav = document.querySelector('.main-nav');
    const whatWeDoSection = document.querySelector('.section-centered');
    
    if (nav) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
                nav.classList.add('shrink');
            } else {
                nav.classList.remove('scrolled');
                nav.classList.remove('shrink');
            }
            
            // Hide navbar completely in "What We Do" section for pure full screen
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
            }
        });
    }

    // ----- Full Page Snap Scrolling -----
    const snapSections = Array.from(document.querySelectorAll('.snap-section'));
    let isSnapping = false;

    if (snapSections.length > 0) {
        window.addEventListener('wheel', function (e) {
            if (isSnapping) return;

            const scrollPos = window.scrollY;
            const threshold = 50; 
            
            // Find current section index based on scroll position
            let currentIndex = -1;
            for (let i = 0; i < snapSections.length; i++) {
                const rect = snapSections[i].getBoundingClientRect();
                if (Math.abs(rect.top) < threshold) {
                    currentIndex = i;
                    break;
                }
            }

            // Only intercept if we are snapped perfectly to a section
            if (currentIndex !== -1) {
                let targetIndex = -1;

                if (e.deltaY > 0 && currentIndex < snapSections.length - 1) {
                    // Scrolling DOWN
                    targetIndex = currentIndex + 1;
                } else if (e.deltaY < 0 && currentIndex > 0) {
                    // Scrolling UP
                    targetIndex = currentIndex - 1;
                }

                if (targetIndex !== -1) {
                    e.preventDefault();
                    isSnapping = true;
                    
                    document.documentElement.style.scrollBehavior = 'auto';
                    
                    const targetPosition = snapSections[targetIndex].getBoundingClientRect().top + scrollPos;
                    const distance = targetPosition - scrollPos;
                    const duration = 300; 
                    let start = null;

                    // Subtle ease in-out quad
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
                }
            }
        }, { passive: false });
    }

    // ----- Scroll Animations (IntersectionObserver) -----
    const animatedElements = document.querySelectorAll('.fade-in, .zoom-in, .fade-in-up, .fade-down');
    if (animatedElements.length > 0) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        animatedElements.forEach(function (el) {
            observer.observe(el);
        });
    }

    // ----- Lightbox -----
    const lightboxOverlay = document.getElementById('lightbox');
    if (lightboxOverlay) {
        const lightboxImg = lightboxOverlay.querySelector('.lightbox-img');
        const lightboxClose = lightboxOverlay.querySelector('.lightbox-close');
        const lightboxPrev = lightboxOverlay.querySelector('.lightbox-prev');
        const lightboxNext = lightboxOverlay.querySelector('.lightbox-next');
        const galleryFigs = document.querySelectorAll('.gallery-fig');
        let currentIndex = 0;

        function openLightbox(index) {
            currentIndex = index;
            const img = galleryFigs[currentIndex].querySelector('img');
            // Use full-res src (remove w1000- prefix if present)
            let src = img.getAttribute('data-full') || img.src;
            lightboxImg.src = src;
            lightboxImg.alt = img.alt || '';
            lightboxOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeLightbox() {
            lightboxOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        function nextImage() {
            currentIndex = (currentIndex + 1) % galleryFigs.length;
            openLightbox(currentIndex);
        }

        function prevImage() {
            currentIndex = (currentIndex - 1 + galleryFigs.length) % galleryFigs.length;
            openLightbox(currentIndex);
        }

        galleryFigs.forEach(function (fig, index) {
            fig.addEventListener('click', function () {
                openLightbox(index);
            });
        });

        if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
        if (lightboxPrev) lightboxPrev.addEventListener('click', prevImage);
        if (lightboxNext) lightboxNext.addEventListener('click', nextImage);

        lightboxOverlay.addEventListener('click', function (e) {
            if (e.target === lightboxOverlay) closeLightbox();
        });

        document.addEventListener('keydown', function (e) {
            if (!lightboxOverlay.classList.contains('active')) return;
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowRight') nextImage();
            if (e.key === 'ArrowLeft') prevImage();
        });
    }

    // ----- Modal Form -----
    const modalOverlay = document.getElementById('quote-modal');
    const modalOpenBtns = document.querySelectorAll('[data-open-modal]');
    const modalCloseBtn = modalOverlay ? modalOverlay.querySelector('.modal-close') : null;

    if (modalOverlay) {
        modalOpenBtns.forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                modalOverlay.classList.add('active');
                document.body.style.overflow = 'hidden';
            });
        });

        if (modalCloseBtn) {
            modalCloseBtn.addEventListener('click', function () {
                modalOverlay.classList.remove('active');
                document.body.style.overflow = '';
            });
        }

        modalOverlay.addEventListener('click', function (e) {
            if (e.target === modalOverlay) {
                modalOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        // Form submission
        const form = modalOverlay.querySelector('form');
        if (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                // Simple feedback
                const btn = form.querySelector('.form-submit');
                btn.textContent = 'Sent!';
                btn.disabled = true;
                setTimeout(function () {
                    modalOverlay.classList.remove('active');
                    document.body.style.overflow = '';
                    form.reset();
                    btn.textContent = 'Send';
                    btn.disabled = false;
                }, 1500);
            });
        }
    }

    // ----- Blog Search & Category Filter -----
    const searchField = document.querySelector('.search-field');
    const categoryItems = document.querySelectorAll('.categories li');
    const blogItems = document.querySelectorAll('.blog-item');

    if (searchField && blogItems.length > 0) {
        searchField.addEventListener('input', function () {
            const query = this.value.toLowerCase();
            blogItems.forEach(function (item) {
                const title = item.getAttribute('data-title') || '';
                const text = item.getAttribute('data-text') || '';
                if (title.includes(query) || text.includes(query)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    if (categoryItems.length > 0 && blogItems.length > 0) {
        categoryItems.forEach(function (cat) {
            cat.addEventListener('click', function () {
                categoryItems.forEach(function (c) { c.classList.remove('active'); });
                this.classList.add('active');
                const category = this.textContent.toLowerCase();

                blogItems.forEach(function (item) {
                    if (category === 'all') {
                        item.style.display = '';
                    } else {
                        const itemCat = item.getAttribute('data-category') || '';
                        if (itemCat.toLowerCase() === category) {
                            item.style.display = '';
                        } else {
                            item.style.display = 'none';
                        }
                    }
                });
            });
        });
    }

    // ----- Horizontal Scroll Active Item & Edge Scroll -----
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
        

        // ----- Parallax Effect -----
        // Create wrappers for parallax so it doesn't conflict with CSS hover scale
        scrollItems.forEach(item => {
            const img = item.querySelector('.item-image img');
            if (img) {
                const wrap = document.createElement('div');
                wrap.className = 'parallax-wrap';
                wrap.style.width = '120%';
                wrap.style.height = '100%';
                wrap.style.marginLeft = '-10%';
                wrap.style.willChange = 'transform';
                img.parentNode.insertBefore(wrap, img);
                wrap.appendChild(img);
            }
        });

        function updateParallax() {
            const center = window.innerWidth / 2;
            scrollItems.forEach(item => {
                const wrap = item.querySelector('.parallax-wrap');
                if (wrap) {
                    const rect = item.getBoundingClientRect();
                    const offset = rect.left + rect.width / 2 - center;
                    const parallaxX = offset * -0.15; // Move opposite to scroll
                    wrap.style.transform = `translateX(${parallaxX}px)`;
                }
            });
        }

        scrollContainer.addEventListener('scroll', () => {
            requestAnimationFrame(updateParallax);
        });
        window.addEventListener('resize', () => requestAnimationFrame(updateParallax));
        updateParallax(); // initial call
    }

});
