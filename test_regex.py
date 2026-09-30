import re
s = '<div class="hero-bg" style="background-image: url('''');"'
print(re.sub(r'(<div class="hero-bg"[^>]*background-image:\s*url\()([^\)]+)(\)[^>]*>)', r'\g<1>NEW\g<3>', s))
