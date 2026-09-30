import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

indicator_logic = """
        // Create Sidebar Indicators
        const indicatorContainer = document.createElement('div');
        indicatorContainer.className = 'section-indicators';
        
        let icons = [
            '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>', // Home
            '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>', // 3 lines
            '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>', // Person
            '<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>' // Envelope
        ];
        
        snapSections.forEach((sec, idx) => {
            const dot = document.createElement('div');
            dot.className = 'indicator-dot';
            if (icons[idx]) {
                dot.innerHTML = icons[idx];
            }
            if (idx === 0) dot.classList.add('active');
            dot.addEventListener('click', () => {
                const scrollPos = window.scrollY;
                const targetPosition = snapSections[idx].getBoundingClientRect().top + scrollPos;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });
            });
            indicatorContainer.appendChild(dot);
        });
        document.body.appendChild(indicatorContainer);
        
        // Update indicators on scroll
        window.addEventListener('scroll', () => {
            let currentIndex = 0;
            let minDiff = Infinity;
            snapSections.forEach((sec, idx) => {
                let diff = Math.abs(sec.getBoundingClientRect().top);
                if (diff < minDiff) {
                    minDiff = diff;
                    currentIndex = idx;
                }
            });
            
            const dots = document.querySelectorAll('.indicator-dot');
            dots.forEach((dot, idx) => {
                if (idx === currentIndex) dot.classList.add('active');
                else dot.classList.remove('active');
            });
        });
"""

# Insert indicator_logic inside `if (snapSections.length > 0) {` block
content = content.replace("if (snapSections.length > 0) {", "if (snapSections.length > 0) {" + indicator_logic)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
