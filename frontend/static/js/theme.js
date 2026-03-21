const getStoredTheme = () => localStorage.getItem('theme');
const setStoredTheme = theme => localStorage.setItem('theme', theme);

const getPreferredTheme = () => {
  const storedTheme = getStoredTheme();
  if (storedTheme) {
    return storedTheme;
  }
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

const setTheme = theme => {
  if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-bs-theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-bs-theme', theme);
  }
};

setTheme(getPreferredTheme());

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  const storedTheme = getStoredTheme();
  if (storedTheme !== 'light' && storedTheme !== 'dark') {
    setTheme(getPreferredTheme());
  }
});

window.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('theme-toggle');
  if(btn) {
    btn.innerHTML = getPreferredTheme() === 'dark' ? '☀️' : '🌙';
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-bs-theme');
      const newTheme = current === 'dark' ? 'light' : 'dark';
      setStoredTheme(newTheme);
      setTheme(newTheme);
      btn.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
    });
  }
  // --- CMD+K Command Palette ---
  const paletteHTML = `
    <div id="cmd-palette-backdrop" class="cmd-backdrop" style="display:none;">
      <div class="cmd-modal">
        <input type="text" id="cmd-input" class="cmd-input" placeholder="Search pages... (e.g. 'Products')" autocomplete="off">
        <div id="cmd-results" class="cmd-results"></div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', paletteHTML);

  const backdrop = document.getElementById('cmd-palette-backdrop');
  const input = document.getElementById('cmd-input');
  const resultsDiv = document.getElementById('cmd-results');
  
  const routes = [
    { name: 'Dashboard', path: 'dashboard.html', icon: '🏠' },
    { name: 'Products', path: 'products.html', icon: '📦' },
    { name: 'Bill of Materials', path: 'bom.html', icon: '🔧' },
    { name: 'Engineering Change Orders', path: 'ecos.html', icon: '📋' },
    { name: 'Reports', path: 'reports.html', icon: '📊' },
    { name: 'Settings', path: 'settings.html', icon: '⚙️' }
  ];

  let activeIndex = 0;
  let currentResults = [];

  const closePalette = () => {
    backdrop.style.display = 'none';
    input.value = '';
    resultsDiv.innerHTML = '';
  };

  const renderResults = (query) => {
    currentResults = routes.filter(r => r.name.toLowerCase().includes(query.toLowerCase()));
    if (!currentResults.length) {
      resultsDiv.innerHTML = '<div class="cmd-item text-muted">No results found</div>';
      return;
    }
    activeIndex = 0;
    resultsDiv.innerHTML = currentResults.map((r, i) => `
      <div class="cmd-item ${i === 0 ? 'active' : ''}" data-path="${r.path}">
        <span class="me-2">${r.icon}</span> ${r.name}
      </div>
    `).join('');
  };

  const updateActive = () => {
    const items = resultsDiv.querySelectorAll('.cmd-item');
    items.forEach((el, i) => {
      if (i === activeIndex) el.classList.add('active');
      else el.classList.remove('active');
    });
  };

  window.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      backdrop.style.display = 'flex';
      input.focus();
      renderResults('');
    }
    if (e.key === 'Escape' && backdrop.style.display === 'flex') {
      closePalette();
    }
  });

  input.addEventListener('input', e => renderResults(e.target.value));

  input.addEventListener('keydown', e => {
    if (!currentResults.length) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeIndex = (activeIndex + 1) % currentResults.length;
      updateActive();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeIndex = (activeIndex - 1 + currentResults.length) % currentResults.length;
      updateActive();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      window.location.href = currentResults[activeIndex].path;
    }
  });

  backdrop.addEventListener('click', e => {
    if (e.target === backdrop) closePalette();
  });

  // --- Navbar Premium Scroll Shadow ---
  const navbar = document.querySelector('.glass-nav');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) navbar.classList.add('scrolled');
      else navbar.classList.remove('scrolled');
    }, { passive: true });
    if (window.scrollY > 10) navbar.classList.add('scrolled');
  }

  // --- Mobile Sidebar Toggle ---
  const sidebar = document.querySelector('.sidebar');
  if (sidebar && navbar) {
    // Inject hamburger button into navbar brand area
    const brand = navbar.querySelector('.navbar-brand');
    if (brand && window.innerWidth <= 991) {
      const toggleBtn = document.createElement('button');
      toggleBtn.className = 'sidebar-toggle';
      toggleBtn.setAttribute('aria-label', 'Open menu');
      toggleBtn.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`;
      navbar.querySelector('.container-fluid').insertBefore(toggleBtn, brand);

      // Backdrop
      const bd = document.createElement('div');
      bd.className = 'sidebar-backdrop';
      document.body.appendChild(bd);

      const openSidebar = () => {
        sidebar.classList.add('show');
        bd.classList.add('show');
        document.body.style.overflow = 'hidden';
        toggleBtn.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;
      };
      const closeSidebar = () => {
        sidebar.classList.remove('show');
        bd.classList.remove('show');
        document.body.style.overflow = '';
        toggleBtn.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`;
      };

      toggleBtn.addEventListener('click', () => {
        sidebar.classList.contains('show') ? closeSidebar() : openSidebar();
      });
      bd.addEventListener('click', closeSidebar);

      // Close sidebar when a nav item is clicked
      sidebar.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', closeSidebar);
      });
    }
  }
});
