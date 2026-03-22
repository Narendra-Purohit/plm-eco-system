import os, glob

# 1. Generate profile.html
profile_html = """<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>PLM — Profile</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="../static/css/main.css">
<script src="../static/js/theme.js"></script>
</head>
<body class="d-flex flex-column min-vh-100 bg-body-tertiary">
<nav class="navbar navbar-expand-lg border-bottom sticky-top glass-nav">
  <div class="container-fluid px-4">
    <a class="navbar-brand fw-bold d-flex align-items-center gap-2" href="dashboard.html">
      <div class="ratio ratio-1x1 rounded ds-logo d-flex align-items-center justify-content-center" style="width: 32px;"><svg viewBox="0 0 40 40" width="18" height="18" xmlns="http://www.w3.org/2000/svg"><circle cx="20" cy="20" r="9" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="3"/><path d="M14 20 A6 6 0 0 1 26 20" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="3" stroke-linecap="round"/><polyline points="24,17 26,20 23,21" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      PLM System
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#topNav"><span class="navbar-toggler-icon"></span></button>
    <div class="collapse navbar-collapse" id="topNav">
      <div class="ms-auto d-flex align-items-center gap-3 mt-3 mt-lg-0">
        <span id="role-badge" class="badge bg-info text-dark rounded-pill px-3 py-2 shadow-sm d-none d-lg-inline-block me-2"></span>
        <button id="theme-toggle" class="btn btn-outline-secondary rounded-circle d-flex align-items-center justify-content-center p-0" style="width:36px;height:36px;" title="Toggle Theme">🌙</button>
        <div class="dropdown">
          <button class="btn btn-primary rounded-circle d-flex align-items-center justify-content-center p-0 shadow-sm transition-all" style="width:36px;height:36px;" id="user-icon" data-bs-toggle="dropdown" aria-expanded="false" title="Profile">👤</button>
          <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0 mt-2" style="min-width: 200px;">
            <li class="px-3 py-2 border-bottom mb-1"><div class="fw-bold text-truncate" id="dropdown-user-name">User</div><div class="text-muted small text-uppercase" id="dropdown-user-role">Role</div></li>
            <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="profile.html"><span class="fs-6">👤</span> View Profile</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item text-danger d-flex align-items-center gap-2 py-2" href="#" onclick="if(confirm('Sign out?')){localStorage.clear();location.href='login.html';}"><span class="fs-6">🚪</span> Sign out</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</nav>

<div class="container-fluid flex-grow-1 d-flex p-0" style="overflow-x: hidden;">
  <div class="sidebar border-end p-3 d-none d-lg-flex flex-column bg-body">
    <div class="small fw-bold text-uppercase text-muted mb-2 px-3 pt-2">Main Menu</div>
    <div class="nav flex-column nav-pills gap-1">
      <a href="dashboard.html" class="nav-link d-flex align-items-center gap-2"><span class="fs-5">🏠</span> Dashboard</a>
      <a href="products.html" class="nav-link d-flex align-items-center gap-2"><span class="fs-5">📦</span> Products</a>
      <a href="bom.html" class="nav-link d-flex align-items-center gap-2"><span class="fs-5">🔧</span> Bill of Materials</a>
      <a href="ecos.html" class="nav-link d-flex align-items-center gap-2"><span class="fs-5">📋</span> ECOs</a>
    </div>
    <div class="small fw-bold text-uppercase text-muted mb-2 px-3 pt-4">Insights</div>
    <div class="nav flex-column nav-pills gap-1">
      <a href="reports.html" class="nav-link d-flex align-items-center gap-2"><span class="fs-5">📊</span> Reports</a>
      <a href="settings.html" class="nav-link d-flex align-items-center gap-2" id="settings-link" style="display:none !important;"><span class="fs-5">⚙️</span> Settings</a>
    </div>
    <div class="mt-auto pt-4">
      <a href="#" class="nav-link text-danger d-flex align-items-center gap-2" onclick="if(confirm('Sign out?')){localStorage.clear();location.href='login.html';}"><span class="fs-5">🚪</span> Sign out</a>
    </div>
  </div>

  <main class="main-content flex-grow-1 p-4 p-md-5 d-flex justify-content-center">
    <div class="card border-0 shadow-sm w-100" style="max-width: 600px; height: fit-content; background: var(--bs-body-bg);">
      <div class="card-body p-5 text-center">
        <div class="rounded-circle bg-primary text-white d-inline-flex align-items-center justify-content-center mb-4 shadow" style="width: 120px; height: 120px; font-size: 3rem;" id="profile-avatar">👤</div>
        <h2 class="fw-bold mb-1" id="profile-name">Loading...</h2>
        <h5 class="text-primary text-uppercase mb-4" id="profile-role">...</h5>
        <div class="row text-start g-3 mt-4 w-100 mx-auto" style="max-width: 400px;">
          <div class="col-12"><div class="p-3 bg-body-tertiary rounded border"><strong>Account ID:</strong> <span class="float-end text-muted" id="profile-id">--</span></div></div>
          <div class="col-12"><div class="p-3 bg-body-tertiary rounded border"><strong>Status:</strong> <span class="float-end badge bg-success-subtle text-success border border-success-subtle rounded-pill">Active</span></div></div>
        </div>
        <hr class="my-5">
        <p class="text-muted small">Profile details are managed centrally by the IT department. If you need to change your role or permissions, contact an Administrator.</p>
        <button class="btn btn-outline-secondary px-4 mt-2" onclick="alert('Profile Edits are restricted.')">Edit Profile</button>
      </div>
    </div>
  </main>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script type="module">
import { api, getCurrentRole, isLoggedIn } from '../static/js/api.js';
if (!isLoggedIn()) { window.location.href = 'login.html'; }
const role = getCurrentRole();
let p = {}; try { p = (typeof getTokenPayload !== 'undefined') ? getTokenPayload() : JSON.parse(atob(localStorage.getItem('token').split('.')[1])); } catch(e){}
const n = p.name || p.first_name || p.username || localStorage.getItem('login_id') || 'User';
const formattedName = n.charAt(0).toUpperCase() + n.slice(1);
const formattedRole = (role || localStorage.getItem('role') || 'Unknown').toUpperCase();

if(document.getElementById('dropdown-user-name')) {
    document.getElementById('dropdown-user-name').textContent = 'User : ' + formattedName;
    document.getElementById('dropdown-user-role').textContent = 'Role : ' + formattedRole;
}
if(document.getElementById('role-badge')) document.getElementById('role-badge').textContent = formattedRole;
if (role === 'admin') document.getElementById('settings-link').style.setProperty('display', 'flex', 'important');

document.getElementById('profile-name').innerHTML = formattedName;
document.getElementById('profile-role').innerHTML = formattedRole;
document.getElementById('profile-id').innerHTML = p.user_id || '--';
document.getElementById('profile-avatar').innerHTML = n.charAt(0).toUpperCase();

</script>
</body>
</html>
"""
with open(r'c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages\profile.html', 'w', encoding='utf-8') as f:
    f.write(profile_html)


# 2. Patch all remaining files missing mt-auto, and inject 'View Profile' link
files = glob.glob(r'c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages\*.html')
skip = ['login.html', 'signup.html', 'profile.html']

for f in files:
    if any(s in f for s in skip): continue
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    # Check if mt-auto exists
    if 'mt-auto pt-4' not in c:
        search_block = '      <a href="settings.html" class="nav-link d-flex align-items-center gap-2" id="settings-link" style="display:none !important;"><span class="fs-5">⚙️</span> Settings</a>\n    </div>\n  </div>'
        replace_block = '      <a href="settings.html" class="nav-link d-flex align-items-center gap-2" id="settings-link" style="display:none !important;"><span class="fs-5">⚙️</span> Settings</a>\n    </div>\n\n    <div class="mt-auto pt-4">\n      <a href="#" class="nav-link text-danger d-flex align-items-center gap-2" onclick="if(confirm(\'Sign out?\')){localStorage.clear();location.href=\'login.html\';}">\n        <span class="fs-5">🚪</span> Sign out\n      </a>\n    </div>\n  </div>'
        c = c.replace(search_block, replace_block)
        
    # Check if View Profile is already in dropdown menu
    if 'View Profile' not in c:
        p1 = '<div class="text-muted small text-uppercase" id="dropdown-user-role">Role</div>\n            </li>'
        p2 = '<div class="text-muted small text-uppercase" id="dropdown-user-role">Role</div>\n            </li>\n            <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="profile.html"><span class="fs-6">👤</span> View Profile</a></li>\n            <li><hr class="dropdown-divider"></li>'
        c = c.replace(p1, p2)
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)
    print("Patched", os.path.basename(f))
print("Profile page and fixes applied.")
