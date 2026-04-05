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
    if (nav) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
                nav.classList.add('shrink');
            } else {
                nav.classList.remove('scrolled');
                nav.classList.remove('shrink');
            }
        });
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

});
