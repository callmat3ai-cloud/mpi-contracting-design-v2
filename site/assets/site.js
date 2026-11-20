/* MPI preview — progressive enhancement only. Content is complete without this file. */
document.documentElement.classList.add('js');

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const head = document.querySelector('.site-head');
const nav = document.getElementById('site-nav');
const menuBtn = document.querySelector('.menu');
const scrim = document.querySelector('.scrim');

/* ---------- header pins after the hero photograph ---------- */
if (head && document.body.classList.contains('t-home')) {
  const pin = () => head.classList.toggle('stuck', window.scrollY > window.innerHeight * 0.6);
  window.addEventListener('scroll', pin, { passive: true });
  pin();
}

/* ---------- reading progress hairline ---------- */
const progress = document.querySelector('[data-progress]');
if (progress) {
  const tick = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = max > 0 ? Math.min(100, (window.scrollY / max) * 100) + '%' : '0%';
  };
  window.addEventListener('scroll', tick, { passive: true });
  window.addEventListener('resize', tick, { passive: true });
  tick();
}

/* ---------- mobile navigation ---------- */
const menuLabel = menuBtn ? menuBtn.querySelector('.menu-label') : null;
function closeNav(returnFocus) {
  if (!nav || !nav.classList.contains('open')) return;
  nav.classList.remove('open');
  menuBtn.classList.remove('is-open');
  if (menuLabel) menuLabel.textContent = 'Menu';
  menuBtn.setAttribute('aria-expanded', 'false');
  if (scrim) scrim.hidden = true;
  document.body.style.overflow = '';
  if (returnFocus) menuBtn.focus();
}
function openNav() {
  nav.classList.add('open');
  menuBtn.classList.add('is-open');
  if (menuLabel) menuLabel.textContent = 'Close';
  menuBtn.setAttribute('aria-expanded', 'true');
  if (scrim) scrim.hidden = false;
  document.body.style.overflow = 'hidden';
  const first = nav.querySelector('a');
  if (first) first.focus();
}
if (menuBtn && nav) {
  menuBtn.addEventListener('click', () => (nav.classList.contains('open') ? closeNav(true) : openNav()));
  if (scrim) scrim.addEventListener('click', () => closeNav(true));
  nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => closeNav(false)));
  document.addEventListener('keydown', (e) => {
    if (!nav.classList.contains('open')) return;
    if (e.key === 'Escape') { closeNav(true); return; }
    if (e.key === 'Tab') {
      const items = [menuBtn, ...nav.querySelectorAll('a')];
      const first = items[0];
      const last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  window.addEventListener('resize', () => { if (window.innerWidth > 800) closeNav(false); });
}

/* ---------- material rail ---------- */
const rail = document.querySelector('[data-rail]');
document.querySelectorAll('[data-gal]').forEach((btn) => {
  btn.addEventListener('click', () => {
    if (!rail) return;
    const card = rail.querySelector('.material');
    const step = card ? card.getBoundingClientRect().width + 20 : 320;
    rail.scrollBy({ left: step * Number(btn.dataset.gal), behavior: reduceMotion ? 'auto' : 'smooth' });
  });
});

/* ---------- demo form (local only, never submits) ---------- */
const form = document.getElementById('estimate');
if (form) {
  const button = document.getElementById('demo');
  const status = document.getElementById('form-status');
  button.disabled = false;
  form.addEventListener('submit', (e) => e.preventDefault());
  button.addEventListener('click', () => {
    if (!form.reportValidity()) {
      status.textContent = 'Check the highlighted fields — nothing has been sent.';
      return;
    }
    status.textContent = 'Demo checked — no request sent. Nothing has been saved. Call MPI to discuss a real project.';
  });
}

/* ---------- motion ---------- */
const gsap = window.gsap;
const ScrollTrigger = window.ScrollTrigger;
if (gsap && ScrollTrigger && !reduceMotion) {
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('motion');

  // headline + intro: one authored entrance
  const heroBits = ['.hero h1 span', '.hero h1 em', '.hero-aside p', '.hero-actions', '.media-credit'];
  const live = heroBits.filter((s) => document.querySelector(s));
  if (live.length) {
    gsap.set(live, { yPercent: 6, autoAlpha: 0 });
    gsap.timeline({ defaults: { ease: 'power3.out' } })
      .from('.hero-rule', { scaleX: 0, duration: 1.5, ease: 'power2.inOut' }, 0)
      .to(live, { yPercent: 0, autoAlpha: 1, duration: 1.05, stagger: 0.09 })
      .from('.hero-media img', { scale: 1.12, duration: 1.6, ease: 'power2.out' }, 0);
  }

  // hero type drifts at a slower rate than the photograph
  const heroTitle = document.querySelector('.hero h1');
  if (heroTitle) {
    gsap.to(heroTitle, {
      yPercent: -12, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 0.5 },
    });
  }

  // image curtains: a threshold opening onto the field
  document.querySelectorAll('.story-media, .division-mast, .detail-mast, .gal-media, .about-media, .voices-media').forEach((box) => {
    gsap.fromTo(box, { clipPath: 'inset(0 0 18% 0)' }, {
      clipPath: 'inset(0 0 0% 0)', duration: 1.25, ease: 'power3.out',
      scrollTrigger: { trigger: box, start: 'top 92%', once: true },
    });
  });

  // section headings settle out of a soft focus
  document.querySelectorAll('.editorial h2, .tech-copy h2, .mat-head h2, .cta h2, .cta-band h2, .about-clients h2, .story-panel h2').forEach((h) => {
    gsap.fromTo(h, { y: 24, opacity: 0, filter: 'blur(7px)' }, {
      y: 0, opacity: 1, filter: 'blur(0px)', duration: 1.05, ease: 'power2.out',
      scrollTrigger: { trigger: h, start: 'top 90%', once: true },
    });
  });

  // section reveals
  document.querySelectorAll('.reveal').forEach((el) => {
    gsap.to(el, {
      y: 0, opacity: 1, duration: 0.95, ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 90%', once: true },
    });
  });

  // chapter chips
  const chapters = gsap.utils.toArray('.chapter');
  if (chapters.length) {
    gsap.from(chapters, {
      y: 22, opacity: 0, duration: 0.8, stagger: 0.07, ease: 'power3.out',
      scrollTrigger: { trigger: '.chapters', start: 'top 96%', once: true },
    });
  }

  // image parallax
  document.querySelectorAll('[data-parallax]').forEach((wrap) => {
    const img = wrap.querySelector('img');
    if (!img) return;
    const amount = Number(wrap.dataset.parallax) || 8;
    gsap.fromTo(img, { yPercent: -amount / 2 }, {
      yPercent: amount / 2, ease: 'none',
      scrollTrigger: { trigger: wrap, start: 'top bottom', end: 'bottom top', scrub: 0.6 },
    });
  });

  // technical line drawing
  document.querySelectorAll('[data-draw]').forEach((svg) => {
    const shapes = svg.querySelectorAll('circle, path');
    shapes.forEach((s) => {
      const len = s.getTotalLength ? s.getTotalLength() : 600;
      gsap.set(s, { strokeDasharray: len, strokeDashoffset: len });
    });
    gsap.to(shapes, {
      strokeDashoffset: 0, duration: 1.9, stagger: 0.1, ease: 'power2.out',
      scrollTrigger: { trigger: svg, start: 'top 82%', once: true },
    });
  });

  window.addEventListener('load', () => ScrollTrigger.refresh());
  // safety: if no trigger registered, never leave content hidden
  setTimeout(() => {
    if (ScrollTrigger.getAll().length === 0) document.documentElement.classList.remove('motion');
  }, 2500);
}

/* ---------- WebGL field: lazy, capped, pausable, decorative ---------- */
const canvas = document.querySelector('[data-field]');
if (canvas && !reduceMotion && window.WebGLRenderingContext) {
  let started = false;
  const boot = () => {
    if (started) return;
    started = true;
    import('./webgl-field.js')
      .then((mod) => mod.mount(canvas))
      .then(() => canvas.classList.add('on'))
      .catch(() => { canvas.style.display = 'none'; });
  };
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { boot(); io.disconnect(); }
    }, { rootMargin: '200px' });
    io.observe(canvas);
  } else {
    boot();
  }
}
