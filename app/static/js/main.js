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

// Premium Dropdown Panels Toggles
const profileTrigger = document.getElementById("profile-trigger");
const profileMenu = document.getElementById("profile-menu");
const notifTrigger = document.getElementById("notification-trigger");
const notifMenu = document.getElementById("notification-menu");

if (profileTrigger && profileMenu) {
  profileTrigger.addEventListener("click", (e) => {
    e.stopPropagation();
    profileMenu.style.display = profileMenu.style.display === "block" ? "none" : "block";
    if (notifMenu) notifMenu.style.display = "none";
  });
}

if (notifTrigger && notifMenu) {
  notifTrigger.addEventListener("click", (e) => {
    e.stopPropagation();
    notifMenu.style.display = notifMenu.style.display === "block" ? "none" : "block";
    if (profileMenu) profileMenu.style.display = "none";
  });
}

document.addEventListener("click", () => {
  if (profileMenu) profileMenu.style.display = "none";
  if (notifMenu) notifMenu.style.display = "none";
});

// Autocomplete Search Bar Implementation
const searchInput = document.getElementById("global-search");
const searchDropdown = document.getElementById("global-search-results");

if (searchInput && searchDropdown) {
  searchInput.addEventListener("input", async (e) => {
    const val = e.target.value.trim();
    if (val.length < 2) {
      searchDropdown.style.display = "none";
      searchDropdown.innerHTML = "";
      return;
    }

    try {
      const res = await fetch(`/api/patients?q=${encodeURIComponent(val)}`);
      if (!res.ok) throw new Error("Search API not accessible or offline");
      const patients = await res.json();
      
      if (patients.length === 0) {
        searchDropdown.style.display = "block";
        searchDropdown.innerHTML = `<div class="autocomplete-item"><span class="autocomplete-item-name" style="color:var(--muted)">No matching patients found</span></div>`;
        return;
      }

      searchDropdown.style.display = "block";
      searchDropdown.innerHTML = patients.map(p => `
        <div class="autocomplete-item" onclick="location.href='/dashboard/clinical#clinical-notes'">
          <div class="autocomplete-item-left">
            <span class="autocomplete-item-name">${p.first_name} ${p.last_name}</span>
            <span class="autocomplete-item-sub">${p.age} yrs · ${p.gender} · ${p.region}</span>
          </div>
          <span class="autocomplete-item-badge bg-${p.risk_category.toLowerCase()}">${p.risk_category}</span>
        </div>
      `).join("");
    } catch (err) {
      // Offline/Local search fallback for demonstration purposes
      const mockMatches = [
        { first_name: "John", last_name: "Doe", age: 45, gender: "Male", region: "North", risk_category: "Critical" },
        { first_name: "Maria", last_name: "Santos", age: 52, gender: "Female", region: "South", risk_category: "Monitoring" },
        { first_name: "Robert", last_name: "Brown", age: 60, gender: "Male", region: "West", risk_category: "Stable" }
      ].filter(p => `${p.first_name} ${p.last_name}`.toLowerCase().includes(val.toLowerCase()));

      if (mockMatches.length > 0) {
        searchDropdown.style.display = "block";
        searchDropdown.innerHTML = mockMatches.map(p => `
          <div class="autocomplete-item" onclick="alert('Viewing detail for ${p.first_name} ${p.last_name}')">
            <div class="autocomplete-item-left">
              <span class="autocomplete-item-name">${p.first_name} ${p.last_name}</span>
              <span class="autocomplete-item-sub">${p.age} yrs · ${p.gender} · ${p.region}</span>
            </div>
            <span class="autocomplete-item-badge bg-${p.risk_category.toLowerCase()}">${p.risk_category}</span>
          </div>
        `).join("");
      } else {
        searchDropdown.style.display = "none";
      }
    }
  });

  searchInput.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  document.addEventListener("click", () => {
    searchDropdown.style.display = "none";
  });
}

