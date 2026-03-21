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
});
