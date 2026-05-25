/**
 * Mjolnir Interactions — Magnetic Hover Effects and Visual Enhancements
 * 
 * Provides smooth cursor glow, magnetic card effects, and navigation sweep animations.
 * Disabled for users with prefers-reduced-motion.
 */
(function () {
  "use strict";

  // Check for reduced motion preference
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /**
   * Initialize cursor glow effect that follows mouse movement
   * Only enabled for devices with proper hover and pointer support
   */
  function initCursorGlow() {
    const glow = document.getElementById("cursor-glow");
    if (!glow || reducedMotion) return;
    
    // Only show glow on devices with fine pointer (mouse, trackpad)
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;

    let x = 0;
    let y = 0;
    let targetX = 0;
    let targetY = 0;

    document.addEventListener("mousemove", function (e) {
      targetX = e.clientX;
      targetY = e.clientY;
      glow.classList.add("is-active");
    });

    /**
     * Smooth animation loop using easing for fluid cursor following
     */
    function animate() {
      // Easing for smooth movement
      x += (targetX - x) * 0.12;
      y += (targetY - y) * 0.12;
      glow.style.transform = `translate(${x}px, ${y}px)`;
      requestAnimationFrame(animate);
    }
    animate();
  }

  /**
   * Initialize magnetic hover effects for cards and buttons
   */
  function initMagnetic() {
    if (reducedMotion) return;

    // Magnetic card rotation effect
    const cards = document.querySelectorAll(".mjolnir-card");
    cards.forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        const rect = card.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        // Calculate rotation based on cursor position
        const rotationX = (e.clientY - centerY) / rect.height;
        const rotationY = (e.clientX - centerX) / rect.width;
        
        card.style.transform = `perspective(800px) rotateY(${rotationY * 6}deg) rotateX(${-rotationX * 6}deg) translateY(-4px)`;
      });
      
      card.addEventListener("mouseleave", function () {
        card.style.transform = "";
      });
    });

    // Magnetic button translation effect
    const buttons = document.querySelectorAll(".mjolnir-btn");
    buttons.forEach(function (btn) {
      btn.addEventListener("mousemove", function (e) {
        const rect = btn.getBoundingClientRect();
        const distanceX = ((e.clientX - rect.left) / rect.width - 0.5) * 8;
        const distanceY = ((e.clientY - rect.top) / rect.height - 0.5) * 8;
        btn.style.transform = `translate(${distanceX}px, ${distanceY}px)`;
      });
      
      btn.addEventListener("mouseleave", function () {
        btn.style.transform = "";
      });
    });
  }

  /**
   * Initialize Bifrost sweep animation on navigation links
   */
  function initBifrostOnNav() {
    const links = document.querySelectorAll('a[href^="#"]');
    const sweep = document.getElementById("bifrost-sweep");
    if (!sweep || reducedMotion) return;

    links.forEach(function (link) {
      link.addEventListener("click", function () {
        // Reset animation by removing and re-adding class
        sweep.classList.remove("is-active");
        // Force reflow to restart animation
        void sweep.offsetWidth;
        sweep.classList.add("is-active");
        
        // Remove active class after animation completes
        sweep.addEventListener(
          "animationend",
          function handler() {
            sweep.classList.remove("is-active");
            sweep.removeEventListener("animationend", handler);
          },
          { once: true }
        );
      });
    });
  }

  /**
   * Initialize all effects
   */
  function init() {
    initCursorGlow();
    initMagnetic();
    initBifrostOnNav();
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
