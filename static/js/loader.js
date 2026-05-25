/**
 * Thunder loading screen — cinematic reveal
 */
(function () {
  "use strict";

  const LOADER_ID = "thunder-loader";
  const BAR_ID = "loader-bar-fill";
  const PERCENT_ID = "loader-percent";
  const MIN_DURATION = 1800;
  const MAX_DURATION = 3200;

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function initLoader() {
    const loader = document.getElementById(LOADER_ID);
    const bar = document.getElementById(BAR_ID);
    const percentEl = document.getElementById(PERCENT_ID);
    if (!loader) return;

    document.body.classList.add("is-loading");

    if (prefersReducedMotion()) {
      finish(loader, bar, percentEl, 0);
      return;
    }

    const start = performance.now();
    const duration = MIN_DURATION + Math.random() * (MAX_DURATION - MIN_DURATION);
    let progress = 0;

    function tick(now) {
      const elapsed = now - start;
      const target = Math.min(100, (elapsed / duration) * 100);
      progress += (target - progress) * 0.12;

      if (bar) bar.style.width = progress + "%";
      if (percentEl) percentEl.textContent = Math.floor(progress) + "%";

      if (elapsed < duration || progress < 99) {
        requestAnimationFrame(tick);
      } else {
        if (bar) bar.style.width = "100%";
        if (percentEl) percentEl.textContent = "100%";
        setTimeout(function () {
          finish(loader, bar, percentEl, 400);
        }, 200);
      }
    }

    requestAnimationFrame(tick);
  }

  function finish(loader, bar, percentEl, delay) {
    setTimeout(function () {
      loader.classList.add("is-exiting");
      document.body.classList.remove("is-loading");

      const sweep = document.getElementById("bifrost-sweep");
      if (sweep) {
        sweep.classList.add("is-active");
        sweep.addEventListener(
          "animationend",
          function () {
            sweep.classList.remove("is-active");
          },
          { once: true }
        );
      }

      setTimeout(function () {
        loader.setAttribute("aria-hidden", "true");
        loader.style.display = "none";
        document.dispatchEvent(new CustomEvent("thunder:loaded"));
      }, 500);
    }, delay);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initLoader);
  } else {
    initLoader();
  }
})();
