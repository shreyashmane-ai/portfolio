/**
 * Storm particle background — canvas ambient energy
 */
(function () {
  "use strict";

  const canvas = document.getElementById("particle-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let particles = [];
  let w = 0;
  let h = 0;
  let rafId = null;
  let reducedMotion = false;

  function init() {
    reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    resize();
    createParticles();
    window.addEventListener("resize", debounce(resize, 150));

    if (!reducedMotion) {
      loop();
    } else {
      drawStatic();
    }
  }

  function debounce(fn, ms) {
    let t;
    return function () {
      clearTimeout(t);
      t = setTimeout(fn, ms);
    };
  }

  function resize() {
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = w;
    canvas.height = h;
    if (reducedMotion) drawStatic();
  }

  function createParticles() {
    const count = Math.min(80, Math.floor((w * h) / 18000));
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.8 + 0.4,
        vx: (Math.random() - 0.5) * 0.25,
        vy: (Math.random() - 0.5) * 0.25,
        alpha: Math.random() * 0.5 + 0.15,
        hue: Math.random() > 0.5 ? 190 : 270,
      });
    }
  }

  function drawStatic() {
    ctx.clearRect(0, 0, w, h);
    particles.forEach(function (p) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(0, 212, 255, " + p.alpha * 0.5 + ")";
      ctx.fill();
    });
  }

  function loop() {
    ctx.clearRect(0, 0, w, h);

    particles.forEach(function (p, i) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      const color =
        p.hue === 190
          ? "rgba(0, 212, 255, " + p.alpha + ")"
          : "rgba(124, 58, 237, " + p.alpha * 0.8 + ")";
      ctx.fillStyle = color;
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        const q = particles[j];
        const dx = p.x - q.x;
        const dy = p.y - q.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 100) {
          ctx.beginPath();
          ctx.strokeStyle = "rgba(0, 212, 255, " + (0.08 * (1 - dist / 100)) + ")";
          ctx.lineWidth = 0.5;
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.stroke();
        }
      }
    });

    if (Math.random() < 0.002) {
      flashLightning();
    }

    rafId = requestAnimationFrame(loop);
  }

  function flashLightning() {
    ctx.save();
    ctx.globalAlpha = 0.04 + Math.random() * 0.06;
    ctx.fillStyle = "#00d4ff";
    ctx.fillRect(0, 0, w, h);
    ctx.restore();
  }

  document.addEventListener("thunder:loaded", function () {
    if (!rafId && !reducedMotion) loop();
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
