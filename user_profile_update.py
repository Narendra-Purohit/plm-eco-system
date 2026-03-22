import os, glob, re

files = glob.glob(r'c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages\*.html')
skip = ['login.html', 'signup.html']

dropdown_html = """<div class="dropdown">
          <button class="btn btn-primary rounded-circle d-flex align-items-center justify-content-center p-0 shadow-sm transition-all" style="width:36px;height:36px;" id="user-icon" data-bs-toggle="dropdown" aria-expanded="false" title="Profile">
            👤
          </button>
          <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0 mt-2" style="min-width: 200px;">
            <li class="px-3 py-2 border-bottom mb-1">
              <div class="fw-bold text-truncate" id="dropdown-user-name">User</div>
              <div class="text-muted small text-uppercase" id="dropdown-user-role">Role</div>
            </li>
            <li><a class="dropdown-item text-danger d-flex align-items-center gap-2 py-2" href="#" onclick="if(confirm('Sign out?')){localStorage.clear();location.href='login.html';}"><span class="fs-6">🚪</span> Sign out</a></li>
          </ul>
        </div>"""

sidebar_logout = """
    <div class="mt-auto pt-4">
      <a href="#" class="nav-link text-danger d-flex align-items-center gap-2" onclick="if(confirm('Sign out?')){localStorage.clear();location.href='login.html';}">
        <span class="fs-5">🚪</span> Sign out
      </a>
    </div>
  </div>

  <!-- Main Content -->"""

for f in files:
    if any(s in f for s in skip): continue
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    # 1. Navbar Dropdown
    c = re.sub(r'<button[^>]*id="user-icon"[^>]*>[\s\S]*?</button>', dropdown_html, c)
    
    # 2. Sidebar Flex & Logout
    c = c.replace('d-none d-lg-block bg-body', 'd-none d-lg-flex flex-column bg-body')
    if '<!-- Main Content -->' in c and 'mt-auto pt-4' not in c:
        c = c.replace('  </div>\n\n  <!-- Main Content -->', sidebar_logout)
        c = c.replace('  </div>\n  <!-- Main Content -->', sidebar_logout)

    # 3. Clean up loose old JS event listeners 
    c = re.sub(r"document\.getElementById\('user-icon'\)\.addEventListener\('click', \(\) => \{[\s\S]*?\}\);", "", c)
    
    # 4. Inject JS for Dropdown User Name
    for s in ["const role = getCurrentRole();", "const role  = getCurrentRole();", "const role = getCurrentRole() || localStorage.getItem('role');"]:
        if s in c and 'dropdown-user-name' not in c:
            js = f"{s}\nif(document.getElementById('dropdown-user-name')) {{\n  const p = getTokenPayload() || {{}}; const n = p.name || p.first_name || p.username || localStorage.getItem('login_id') || 'User';\n  document.getElementById('dropdown-user-name').textContent = n.charAt(0).toUpperCase() + n.slice(1);\n  document.getElementById('dropdown-user-role').textContent = role?.toUpperCase();\n}}"
            c = c.replace(s, js)
            break

    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)
    print("Updated", os.path.basename(f))
print("All files processed.")
