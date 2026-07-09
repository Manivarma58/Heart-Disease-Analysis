document.querySelectorAll(".tableau-embed").forEach((target) => {
  const url = target.dataset.tableauUrl;
  if (!url) return;
  const iframe = document.createElement("iframe");
  iframe.src = url;
  iframe.title = "Embedded Tableau dashboard";
  iframe.loading = "lazy";
  iframe.referrerPolicy = "strict-origin-when-cross-origin";
  iframe.style.width = "100%";
  iframe.style.minHeight = "520px";
  iframe.style.border = "0";
  target.appendChild(iframe);
});
