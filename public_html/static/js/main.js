// ================= Mobile Menu =================
const menuBtn = document.getElementById('menuBtn');
const drawer = document.getElementById('drawer');

if (menuBtn && drawer) {
  menuBtn.addEventListener('click', () => {
    drawer.classList.toggle('open');
    drawer.style.display =
      drawer.style.display === 'block' ? 'none' : 'block';
  });
}

// ================= Scroll Reveal =================
const reveals = document.querySelectorAll('.reveal');

if (reveals.length) {
  const io = new IntersectionObserver(
    entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('reveal-active');
          io.unobserve(e.target);
        }
      });
    },
    { threshold: 0.2 }
  );

  reveals.forEach(el => io.observe(el));
}

// ================= Footer Year =================
const yearEl = document.getElementById('year');
if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

// ================= Hero Parallax =================
const hero = document.querySelector('.hero');
const orbs = document.querySelectorAll('.orb');

if (hero && orbs.length && window.innerWidth > 900) {
  let mouseX = 0;
  let mouseY = 0;
  let rafId = null;

  const onMouseMove = e => {
    const rect = hero.getBoundingClientRect();
    mouseX = (e.clientX - rect.left) / rect.width - 0.5;
    mouseY = (e.clientY - rect.top) / rect.height - 0.5;

    if (!rafId) {
      rafId = requestAnimationFrame(updateParallax);
    }
  };

  const updateParallax = () => {
    orbs.forEach((orb, index) => {
      const strength = (index + 1) * 12;
      orb.style.transform = `translate3d(
        ${mouseX * strength}px,
        ${mouseY * strength}px,
        0
      )`;
    });
    rafId = null;
  };

  hero.addEventListener('mousemove', onMouseMove);
}

// ================= Scroll To Top =================
const toTop = document.getElementById('toTop');

if (toTop) {
  window.addEventListener('scroll', () => {
    toTop.classList.toggle('show', window.scrollY > 300);
  });

  toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ================= Preloader (BULLETPROOF) =================
(function () {
  const preloader = document.getElementById("preloader");
  if (!preloader) return;

  const hide = () => {
    preloader.classList.add("hide");

    setTimeout(() => {
      preloader.remove();
    }, 700);
  };

  // Always hide after page is usable
  window.addEventListener("load", hide, { once: true });

  // Absolute fallback
  setTimeout(hide, 3000);
})();



document.querySelectorAll(".faq-card").forEach(card => {
    card.addEventListener("click", () => {

        // Close all others
        document.querySelectorAll(".faq-card").forEach(c => {
            if (c !== card) {
                c.classList.remove("active");
            }
        });

        // Toggle current
        card.classList.toggle("active");
    });
});


