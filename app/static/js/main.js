if (window.lucide) {
  window.lucide.createIcons();
}

document.querySelectorAll(".toast").forEach((toast) => {
  setTimeout(() => toast.remove(), 5200);
});
