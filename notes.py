import re

with open('script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to refactor the horizontal scroll logic into a reusable function
# and call it for both .linkpage-grid and .team-grid

# Wait, it's easier to just append the initialization for team-grid
# But the team-grid doesn't have parallax wrap (or maybe it does?).
# Let's write a small addition to script.js
