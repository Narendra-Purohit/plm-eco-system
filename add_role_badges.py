import os, glob
files = glob.glob(r'c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages\*.html')
skip = ['login.html', 'signup.html', 'dashboard.html']
for f in files:
    if any(s in f for s in skip): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    changed = False
    
    # Add HTML
    if 'id="role-badge"' not in content:
        content = content.replace(
            '<button id="theme-toggle"',
            '<span id="role-badge" class="badge bg-info text-dark rounded-pill px-3 py-2 shadow-sm d-none d-md-inline-block me-2"></span>\n        <button id="theme-toggle"'
        )
        changed = True
        
    # Add JS
    if "document.getElementById('role-badge')" not in content:
        search = "const role = getCurrentRole();"
        if search in content:
            js = "\nif(document.getElementById('role-badge')) document.getElementById('role-badge').textContent = role?.toUpperCase();\n"
            content = content.replace(search, search + js, 1)
            changed = True
        else:
            search = "const role  = getCurrentRole();"
            if search in content:
                js = "\nif(document.getElementById('role-badge')) document.getElementById('role-badge').textContent = role?.toUpperCase();\n"
                content = content.replace(search, search + js, 1)
                changed = True
    if changed:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print("Updated", os.path.basename(f))
print("Done.")
