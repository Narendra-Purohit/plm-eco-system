import os, glob

files = glob.glob(r'c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages\*.html')
skip = ['login.html', 'signup.html', 'dashboard.html']

for f in files:
    if any(s in f for s in skip): continue
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
        
    # Remove existing role badge HTML
    if '<span id="role-badge"' in c:
        start = c.find('<span id="role-badge"')
        end = c.find('</span>', start) + 7
        c = c[:start] + c[end:]
        
    # Insert fresh HTML right before theme-toggle
    c = c.replace(
        '<button id="theme-toggle"',
        '<span id="role-badge" class="badge bg-info text-dark rounded-pill px-3 py-2 shadow-sm d-none d-lg-inline-block me-2"></span>\n        <button id="theme-toggle"'
    )
    
    # Remove all existing JS
    c = c.replace("if(document.getElementById('role-badge')) document.getElementById('role-badge').textContent = role?.toUpperCase();\n", '')
    c = c.replace("    if(document.getElementById('role-badge')) document.getElementById('role-badge').textContent = role?.toUpperCase();\n", '')
    
    # Inject fresh JS after 'getCurrentRole()'
    for s in ["const role = getCurrentRole();", "const role  = getCurrentRole();"]:
        if s in c:
            js = f"{s}\nif(document.getElementById('role-badge')) document.getElementById('role-badge').textContent = role?.toUpperCase();"
            c = c.replace(s, js)
            break
            
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)
    print("Fixed", os.path.basename(f))
print("All files perfectly synchronized.")
