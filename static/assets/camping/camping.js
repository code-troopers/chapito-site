const header = document.querySelector('[data-header]');
const menuToggle = document.querySelector('.menu-toggle');
const mainNavigation = document.querySelector('.main-nav');
const situationTabs = [...document.querySelectorAll('.situation-tab')];
const situationPanel = document.querySelector('#situation-panel');
const situationScreen = document.querySelector('[data-situation-screen]');
const situationAnswers = [...document.querySelectorAll('.situation-answer')];
const adminTabs = [...document.querySelectorAll('.admin-tab')];
const adminScreen = document.querySelector('[data-admin-screen]');
const adminCaption = document.querySelector('[data-admin-caption]');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

document.documentElement.classList.add('motion-ready');

const closeMenu = () => {
  mainNavigation?.classList.remove('open');
  menuToggle?.setAttribute('aria-expanded', 'false');
  const label = menuToggle?.querySelector('.sr-only');
  if (label) label.textContent = 'Ouvrir le menu';
};

const updateHeader = () => header?.classList.toggle('scrolled', window.scrollY > 10);

updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

menuToggle?.addEventListener('click', () => {
  const isOpen = mainNavigation.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
  menuToggle.querySelector('.sr-only').textContent = isOpen ? 'Fermer le menu' : 'Ouvrir le menu';
});

mainNavigation?.addEventListener('click', (event) => {
  if (event.target.closest('a')) closeMenu();
});

const selectSituation = (tab) => {
  situationTabs.forEach((item) => {
    const isActive = item === tab;
    item.classList.toggle('active', isActive);
    item.setAttribute('aria-selected', String(isActive));
    item.tabIndex = isActive ? 0 : -1;
  });

  situationScreen?.classList.add('changing');
  window.setTimeout(() => {
    if (situationScreen) {
      situationScreen.src = tab.dataset.src;
      situationScreen.alt = tab.dataset.alt;
      situationScreen.classList.remove('changing');
    }
  }, reducedMotion.matches ? 0 : 170);

  // les quatre réponses occupent la même place : seule la visibilité change, la hauteur du bloc reste fixe
  situationAnswers.forEach((answer) => answer.classList.toggle('is-active', answer.dataset.answerFor === tab.id));
  situationPanel?.setAttribute('aria-labelledby', tab.id);
};

situationTabs.forEach((tab) => {
  tab.addEventListener('click', () => selectSituation(tab));
  tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = situationTabs.indexOf(tab);
    if (event.key === 'Home') nextIndex = 0;
    else if (event.key === 'End') nextIndex = situationTabs.length - 1;
    else nextIndex = (nextIndex + (['ArrowRight', 'ArrowDown'].includes(event.key) ? 1 : -1) + situationTabs.length) % situationTabs.length;
    situationTabs[nextIndex].focus();
    selectSituation(situationTabs[nextIndex]);
  });
});

const selectAdminScreen = (tab) => {
  adminTabs.forEach((item) => {
    const isActive = item === tab;
    item.classList.toggle('active', isActive);
    item.setAttribute('aria-selected', String(isActive));
    item.tabIndex = isActive ? 0 : -1;
  });

  adminScreen?.classList.add('changing');
  window.setTimeout(() => {
    if (adminScreen) {
      adminScreen.src = tab.dataset.src;
      adminScreen.alt = tab.dataset.alt;
      adminScreen.classList.remove('changing');
    }
  }, reducedMotion.matches ? 0 : 170);
  if (adminCaption) adminCaption.textContent = tab.dataset.caption;
};

adminTabs.forEach((tab) => {
  tab.addEventListener('click', () => selectAdminScreen(tab));
  tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = adminTabs.indexOf(tab);
    if (event.key === 'Home') nextIndex = 0;
    else if (event.key === 'End') nextIndex = adminTabs.length - 1;
    else nextIndex = (nextIndex + (event.key === 'ArrowRight' ? 1 : -1) + adminTabs.length) % adminTabs.length;
    adminTabs[nextIndex].focus();
    selectAdminScreen(adminTabs[nextIndex]);
  });
});

const heroPhones = document.querySelector('.hero-phones');
window.requestAnimationFrame(() => heroPhones?.classList.add('is-ready'));

const revealItems = [...document.querySelectorAll('.reveal')];
if (reducedMotion.matches || !('IntersectionObserver' in window)) {
  revealItems.forEach((item) => item.classList.add('is-visible'));
} else {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.14 });
  revealItems.forEach((item) => revealObserver.observe(item));
}
