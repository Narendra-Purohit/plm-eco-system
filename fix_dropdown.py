import os, glob, re

files = glob.glob(r'c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages\*.html')
skip = ['login.html', 'signup.html']

for f in files:
    if any(s in f for s in skip): continue
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    # Check if we already injected JS
    if "User :" in c and "Role :" in c:
        continue
        
    js = """
if(document.getElementById('dropdown-user-name')) {
    let p = {};
    try { p = (typeof getTokenPayload !== 'undefined') ? getTokenPayload() : JSON.parse(atob(localStorage.getItem('token').split('.')[1])); } catch(e){}
    const n = p.name || p.first_name || p.username || localStorage.getItem('login_id') || 'User';
    document.getElementById('dropdown-user-name').textContent = 'User : ' + n;
    document.getElementById('dropdown-user-role').textContent = 'Role : ' + (role || localStorage.getItem('role') || 'Unknown').toUpperCase();
}
"""
    # Remove any old JS we might have partially injected
    c = re.sub(r'if\s*\(\s*document\.getElementById\(\s*\'dropdown-user-name\'\s*\)\s*\)\s*\{[\s\S]*?\}', '', c)
    
    # Re-inject correct JS
    for s in ["const role = getCurrentRole();", "const role  = getCurrentRole();", "const role = getCurrentRole() || localStorage.getItem('role');"]:
        if s in c:
            c = c.replace(s, s + js)
            break

    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)
    print("Fixed JS for", os.path.basename(f))
print("All JS updated.")
