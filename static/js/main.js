// ─── FLEXPLAN MAIN JS ───────────────────────────────────────────────────────

// Active nav link
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path || (path === '/' && href === '/') || (path !== '/' && href !== '/' && path.startsWith(href))) {
      a.classList.add('active');
    }
  });

  // Load auth state
  loadAuthState();
});

async function loadAuthState() {
  try {
    const res = await fetch('/api/me');
    const data = await res.json();
    const navAuth = document.getElementById('nav-auth');
    if (!navAuth) return;
    if (data.logged_in) {
      navAuth.innerHTML = `
        <span class="nav-user">👋 ${data.username}</span>
        <button onclick="logout()" class="btn-secondary" style="padding:0.4rem 1rem;font-size:0.85rem">Logout</button>
      `;
    } else {
      navAuth.innerHTML = `
        <a href="/login" class="btn-secondary" style="padding:0.45rem 1rem;font-size:0.85rem">Login</a>
        <a href="/register" class="nav-cta nav-links a" style="padding:0.45rem 1.1rem;font-size:0.85rem;background:var(--orange);color:#fff;border-radius:8px;font-weight:600;text-decoration:none">Register</a>
      `;
    }
  } catch (e) {}
}

async function logout() {
  await fetch('/api/logout', { method: 'POST' });
  window.location.reload();
}
