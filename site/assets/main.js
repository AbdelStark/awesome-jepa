(() => {
  const dataEl = document.getElementById("site-data");
  const data = dataEl ? JSON.parse(dataEl.textContent) : { headings: [] };

  const search = document.getElementById("resource-search");
  const items = Array.from(document.querySelectorAll(".resource-item"));

  function normalize(value) {
    return value.toLowerCase().replace(/\s+/g, " ").trim();
  }

  function applyFilter() {
    const query = normalize(search.value);
    for (const item of items) {
      item.hidden = query.length > 0 && !normalize(item.textContent).includes(query);
    }
  }

  if (search) {
    search.addEventListener("input", applyFilter);
  }

  const links = Array.from(document.querySelectorAll(".toc-link"));
  const sections = links
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  if ("IntersectionObserver" in window && sections.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (!visible) return;
        for (const link of links) {
          link.classList.toggle("is-active", link.getAttribute("href") === `#${visible.target.id}`);
        }
      },
      { rootMargin: "-20% 0px -70% 0px", threshold: [0.1, 0.4, 0.8] },
    );
    for (const section of sections) observer.observe(section);
  }

  const canvas = document.getElementById("latent-map");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const palette = ["#d8a925", "#bb3d2a", "#5e87a6", "#6da56d", "#e7d79a"];
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const pointer = { x: 0.72, y: 0.36, active: false };
  let points = [];
  let frame = 0;

  function hash(value) {
    let acc = 0;
    for (let i = 0; i < value.length; i += 1) {
      acc = (acc * 31 + value.charCodeAt(i)) >>> 0;
    }
    return acc;
  }

  function rebuildPoints() {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    points = data.headings.map((heading, index) => {
      const h = hash(heading.slug);
      const ring = heading.level === 2 ? 0.3 : 0.46;
      const angle = (index / Math.max(1, data.headings.length)) * Math.PI * 2 + (h % 19) * 0.07;
      return {
        x: width * (0.62 + Math.cos(angle) * ring * 0.65),
        y: height * (0.5 + Math.sin(angle) * ring),
        baseX: width * (0.62 + Math.cos(angle) * ring * 0.65),
        baseY: height * (0.5 + Math.sin(angle) * ring),
        radius: 3.5 + Math.sqrt(Math.max(1, heading.resource_count)) * 1.25,
        color: palette[index % palette.length],
        phase: (h % 360) * (Math.PI / 180),
        title: heading.title,
      };
    });
  }

  function resize() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(canvas.clientWidth * ratio);
    canvas.height = Math.floor(canvas.clientHeight * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    rebuildPoints();
    draw();
  }

  function draw() {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#10140f";
    ctx.fillRect(0, 0, width, height);

    const centerX = width * 0.64;
    const centerY = height * 0.5;
    frame += reducedMotion ? 0 : 0.008;

    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, width * 0.58);
    gradient.addColorStop(0, "rgba(94, 135, 166, 0.20)");
    gradient.addColorStop(0.46, "rgba(45, 107, 79, 0.10)");
    gradient.addColorStop(1, "rgba(16, 20, 15, 0)");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);

    for (const point of points) {
      const drift = reducedMotion ? 0 : Math.sin(frame + point.phase) * 7;
      point.x = point.baseX + drift;
      point.y = point.baseY + Math.cos(frame * 0.8 + point.phase) * 5;
      if (pointer.active) {
        point.x += (pointer.x * width - point.x) * 0.018;
        point.y += (pointer.y * height - point.y) * 0.018;
      }

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(point.x, point.y);
      ctx.strokeStyle = "rgba(251, 252, 247, 0.08)";
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    ctx.beginPath();
    ctx.arc(centerX, centerY, 11, 0, Math.PI * 2);
    ctx.fillStyle = "#f4f7f0";
    ctx.fill();

    for (const point of points) {
      ctx.beginPath();
      ctx.arc(point.x, point.y, point.radius + 7, 0, Math.PI * 2);
      ctx.fillStyle = `${point.color}24`;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(point.x, point.y, point.radius, 0, Math.PI * 2);
      ctx.fillStyle = point.color;
      ctx.fill();
    }

    if (!reducedMotion) {
      requestAnimationFrame(draw);
    }
  }

  canvas.addEventListener("pointermove", (event) => {
    const rect = canvas.getBoundingClientRect();
    pointer.x = (event.clientX - rect.left) / rect.width;
    pointer.y = (event.clientY - rect.top) / rect.height;
    pointer.active = true;
  });

  canvas.addEventListener("pointerleave", () => {
    pointer.active = false;
  });

  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(canvas);
})();
