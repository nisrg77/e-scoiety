import re

with open('templates/core/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update font sizes
content = content.replace('"h3": ["32px"', '"h3": ["40px"')
content = content.replace('"button": ["16px"', '"button": ["18px"')
content = content.replace('"body-md": ["16px"', '"body-md": ["18px"')
content = content.replace('"h2": ["48px"', '"h2": ["56px"')
content = content.replace('"h1": ["64px"', '"h1": ["80px"')
content = content.replace('"label-bold": ["14px"', '"label-bold": ["16px"')
content = content.replace('"body-lg": ["18px"', '"body-lg": ["22px"')

# 2. Increase max-width to better use window space
content = content.replace('max-w-7xl', 'max-w-[1500px]')

# 3. Make hero section taller
content = content.replace(
    '<section class="max-w-[1500px] mx-auto px-8 pt-20 pb-32 grid md:grid-cols-2 gap-16 items-center">',
    '<section class="max-w-[1500px] mx-auto px-8 pt-20 pb-32 grid md:grid-cols-2 gap-16 items-center min-h-[calc(100vh-80px)]">'
)

with open('templates/core/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
