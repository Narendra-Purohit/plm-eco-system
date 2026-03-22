import os, glob, re

files = glob.glob(r'c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages\*.html')
skip = ['login.html', 'signup.html']

simple_button = '''<button class="btn btn-primary rounded-circle d-flex align-items-center justify-content-center p-0 shadow-sm transition-all" style="width:36px;height:36px;" id="user-icon" title="View Profile" onclick="location.href=\'profile.html\'">👤</button>'''

for f in files:
    if any(s in f for s in skip): continue
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    # Replace the dropdown block with the simple button
    c = re.sub(r'<div class="dropdown">\s*<button[^>]*id="user-icon"[^>]*>👤</button>\s*<ul class="dropdown-menu[^>]*>[\s\S]*?</ul>\s*</div>', simple_button, c)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)
    print("Updated", os.path.basename(f))
print("Dropdown removed.")
