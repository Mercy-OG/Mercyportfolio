// ── HEADER SCROLL ──
const hdr = document.getElementById('hdr');
const pill = hdr?.querySelector('.nav-pill');
const onScroll = () => hdr?.classList.toggle('scrolled', window.scrollY > 60);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ── MOBILE MENU ──
const mobBtn = document.getElementById('mobBtn');
const navLinks = document.getElementById('navLinks');
const overlay = document.getElementById('mob-overlay');

const openMenu = () => {
  navLinks?.classList.add('open');
  overlay?.classList.add('active');
  if (mobBtn) mobBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
  document.body.style.overflow = 'hidden';
};
const closeMenu = () => {
  navLinks?.classList.remove('open');
  overlay?.classList.remove('active');
  if (mobBtn) mobBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
  document.body.style.overflow = '';
};

mobBtn?.addEventListener('click', () => navLinks?.classList.contains('open') ? closeMenu() : openMenu());
overlay?.addEventListener('click', closeMenu);
navLinks?.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));

// ── SCROLL REVEAL ──
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// ── SMOOTH ANCHOR SCROLL ──
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (!id || id === '#') return;
    const target = document.querySelector(id);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── BUTTON PRESS EFFECT ──
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('mousedown', () => { btn.style.transform = 'translateY(2px) scale(0.975)'; });
  const reset = () => { btn.style.transform = ''; };
  btn.addEventListener('mouseup', reset);
  btn.addEventListener('mouseleave', reset);
});
