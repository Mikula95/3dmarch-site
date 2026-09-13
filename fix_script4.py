import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

init_block = """
        // Initialize current section based on scroll position
        let initialScroll = window.scrollY;
        let closestIndex = 0;
        let minDiff = Infinity;
        snapSections.forEach((sec, idx) => {
            let diff = Math.abs(sec.getBoundingClientRect().top);
            if (diff < minDiff) {
                minDiff = diff;
                closestIndex = idx;
            }
        });
        currentSectionIndex = closestIndex;
        
        // Hide scrollbar and disable native scrolling
"""

content = content.replace("// Hide scrollbar and disable native scrolling", init_block)

# Also need to update indicators on load
init_indicator = """
        document.body.appendChild(indicatorContainer);
        updateIndicators(currentSectionIndex);
"""
content = content.replace("document.body.appendChild(indicatorContainer);", init_indicator)


with open('script.js', 'w', encoding='utf-8') as f:
    f.write(content)
