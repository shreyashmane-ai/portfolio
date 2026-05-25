/**
 * Thunder Command — Core Portfolio Interactions
 * 
 * Handles theme toggling, scroll effects, animations, and form interactions.
 * Respects user's prefers-reduced-motion preference for accessibility.
 */
(function () {
  "use strict";

  // Check for reduced motion preference
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /**
   * Throttle function to limit callback execution frequency
   * @param {Function} fn - Callback to throttle
   * @param {number} wait - Minimum milliseconds between executions
   * @returns {Function} Throttled function
   */
  function throttle(fn, wait) {
    let lastTime = 0;
    return function (...args) {
      const now = Date.now();
      if (now - lastTime >= wait) {
        lastTime = now;
        fn.apply(this, args);
      }
    };
  }

  /**
   * Initialize theme toggle with localStorage persistence
   */
  function initTheme() {
    const root = document.documentElement;
    const toggle = document.getElementById("theme-toggle");
    const stored = localStorage.getItem("thunder-theme");
    const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;
    const theme = stored || (prefersLight ? "light" : "dark");
    
    root.setAttribute("data-theme", theme);
    if (toggle) toggle.setAttribute("aria-pressed", theme === "dark");

    toggle?.addEventListener("click", function () {
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("thunder-theme", next);
      toggle.setAttribute("aria-pressed", next === "dark");
    });
  }

  /**
   * Initialize scrollspy to highlight active nav links
   * Also updates scroll progress indicator
   */
  function initScrollspy() {
    const sections = document.querySelectorAll("section[data-section]");
    const navLinks = document.querySelectorAll(
      '.thunder-nav-pills .nav-link, .sidebar-link, .mobile-nav-list .nav-link'
    );
    const energyBar = document.getElementById("sidebar-energy");

    if (!sections.length) return;

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          const id = entry.target.getAttribute("data-section");
          navLinks.forEach(function (link) {
            const href = link.getAttribute("href");
            link.classList.toggle("active", href === "#" + id);
          });
        });
      },
      { rootMargin: "-40% 0px -50% 0px", threshold: 0 }
    );

    sections.forEach(section => observer.observe(section));

    // Update scroll progress bar
    window.addEventListener(
      "scroll",
      throttle(function () {
        if (!energyBar) return;
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        energyBar.style.width = pct + "%";
      }, 50),
      { passive: true }
    );
  }

  /**
   * Initialize scroll-triggered reveal animations
   */
  function initReveals() {
    const items = document.querySelectorAll(".reveal-up");
    if (reducedMotion) {
      items.forEach(el => el.classList.add("is-visible"));
      return;
    }

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    items.forEach(el => observer.observe(el));
  }

  /**
   * Animate counters when they become visible
   */
  function initCounters() {
    const counters = document.querySelectorAll(".counter");
    if (!counters.length) return;

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting || entry.target.dataset.animated) return;
          entry.target.dataset.animated = "true";
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.5 }
    );

    counters.forEach(counter => observer.observe(counter));
  }

  /**
   * Animate a single counter from 0 to target value
   * @param {HTMLElement} el - Counter element with data-target and data-decimals
   */
  function animateCounter(el) {
    const target = parseFloat(el.dataset.target, 10);
    const decimals = parseInt(el.dataset.decimals || "0", 10);
    const duration = reducedMotion ? 0 : 1600;
    const start = performance.now();

    function tick(now) {
      const elapsed = now - start;
      const progress = duration === 0 ? 1 : Math.min(1, elapsed / duration);
      // Ease out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = target * eased;
      el.textContent = value.toFixed(decimals);
      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        el.textContent = target.toFixed(decimals);
      }
    }
    requestAnimationFrame(tick);
  }

  /**
   * Animate skill proficiency bars on scroll
   */
  function initSkillBars() {
    const bars = document.querySelectorAll(".skills-bar-fill");
    
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.style.width = entry.target.dataset.level + "%";
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.3 }
    );
    
    bars.forEach(bar => observer.observe(bar));
  }

  /**
   * Initialize typing effect for hero roles
   */
  function initTyping() {
    const el = document.getElementById("typed-role");
    if (!el) return;
    
    const roles = (el.dataset.roles || "Python Backend Engineer").split("|");
    
    // Show first role immediately if motion is reduced
    if (reducedMotion) {
      el.textContent = roles[0] || "";
      return;
    }

    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function typeStep() {
      const current = roles[roleIndex];
      if (!isDeleting) {
        el.textContent = current.substring(0, charIndex + 1);
        charIndex++;
        if (charIndex === current.length) {
          isDeleting = true;
          setTimeout(typeStep, 2200);
          return;
        }
      } else {
        el.textContent = current.substring(0, charIndex - 1);
        charIndex--;
        if (charIndex === 0) {
          isDeleting = false;
          roleIndex = (roleIndex + 1) % roles.length;
        }
      }
      setTimeout(typeStep, isDeleting ? 40 : 80);
    }
    typeStep();
  }

  /**
   * Initialize parallax effect for hero dashboard
   */
  function initParallax() {
    if (reducedMotion) return;
    
    const dashboard = document.querySelector(".hero-dashboard");
    if (!dashboard) return;

    window.addEventListener(
      "scroll",
      throttle(function () {
        const y = window.scrollY;
        if (y < window.innerHeight) {
          dashboard.style.transform = "translateY(" + (y * 0.06) + "px)";
        }
      }, 16),
      { passive: true }
    );
  }

  /**
   * Initialize project modal with dynamic content loading
   */
  function initProjectModals() {
    const dataEl = document.getElementById("projects-data");
    if (!dataEl) return;

    let projects = [];
    try {
      projects = JSON.parse(dataEl.textContent);
    } catch (e) {
      console.warn("Failed to parse projects data");
      return;
    }

    const modal = document.getElementById("projectModal");
    if (!modal) return;

    modal.addEventListener("show.bs.modal", function (event) {
      const btn = event.relatedTarget;
      const id = btn?.getAttribute("data-project-id");
      const project = projects.find(p => p.id === id);
      if (!project) return;

      const idx = projects.indexOf(project) + 1;
      document.getElementById("modal-sys-id").textContent = "SYS-" + String(idx).padStart(2, "0");
      document.getElementById("projectModalLabel").textContent = project.title;
      document.getElementById("modal-subtitle").textContent = project.subtitle;
      document.getElementById("modal-description").textContent = project.description;

      // Populate metrics
      const metricsEl = document.getElementById("modal-metrics");
      metricsEl.innerHTML = (project.metrics || [])
        .map(m =>
          `<div class="col-md-4"><div class="modal-metric-box">
            <span class="projects-metric-value d-block">${m.value}</span>
            <span class="projects-metric-label">${m.label}</span>
           </div></div>`
        )
        .join("");

      // Populate tech stack
      const techEl = document.getElementById("modal-tech");
      techEl.innerHTML = (project.tech || [])
        .map(t => `<span class="tech-badge">${t}</span>`)
        .join("");

      // Set links
      const demoLink = document.getElementById("modal-demo");
      const githubLink = document.getElementById("modal-github");
      if (demoLink) demoLink.href = project.demo;
      if (githubLink) githubLink.href = project.github;
    });
  }

  /**
   * Initialize contact form submit animation
   */
  function initContactForm() {
    const form = document.getElementById("contact-form");
    const btn = document.getElementById("contact-submit");
    if (!form || !btn) return;

    form.addEventListener("submit", function () {
      const text = btn.querySelector(".btn-text");
      const loading = btn.querySelector(".btn-loading");
      text?.classList.add("d-none");
      loading?.classList.remove("d-none");
      btn.disabled = true;
    });
  }

  /**
   * Auto-show Bootstrap toasts
   */
  function initToasts() {
    document.querySelectorAll(".thunder-toast").forEach(el => {
      bootstrap.Toast.getOrCreateInstance(el).show();
    });
  }

  /**
   * Initialize scroll-triggered animations
   */
  function onScrolledToPage() {
    initReveals();
    initCounters();
    initSkillBars();
  }

  /**
   * Main initialization — call all setup functions
   */
  function init() {
    initTheme();
    initScrollspy();
    initTyping();
    initParallax();
    initProjectModals();
    initContactForm();
    initToasts();
    onScrolledToPage();
  }

  // Re-initialize on dynamic content load
  document.addEventListener("thunder:loaded", onScrolledToPage);

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
