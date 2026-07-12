if (window.lucide) {
  window.lucide.createIcons();
}

document.querySelectorAll(".toast").forEach((toast) => {
  setTimeout(() => toast.remove(), 5200);
});

document.querySelectorAll("[data-viz-width]").forEach((element) => {
  element.style.width = `${element.dataset.vizWidth}%`;
});

document.querySelectorAll("[data-viz-height]").forEach((element) => {
  element.style.height = `${element.dataset.vizHeight}px`;
});

document.querySelectorAll("[data-viz-height-pct]").forEach((element) => {
  element.style.height = `${element.dataset.vizHeightPct}%`;
});

document.querySelectorAll("[data-viz-size]").forEach((element) => {
  element.style.setProperty("--size", `${element.dataset.vizSize}px`);
});
