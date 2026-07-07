const search = document.querySelector("#patient-search");
const results = document.querySelector("#patient-results");

function badgeClass(category) {
  return String(category || "").toLowerCase();
}

if (search && results) {
  search.addEventListener("input", async (event) => {
    const q = event.target.value.trim();
    if (q.length < 2) return;
    const response = await fetch(`/api/patients?q=${encodeURIComponent(q)}`);
    const patients = await response.json();
    results.innerHTML = patients.map((patient) => `
      <article class="patient-card">
        <div class="patient-top">
          <span class="avatar">${patient.first_name[0]}${patient.last_name[0]}</span>
          <span class="badge ${badgeClass(patient.risk_category)}">${patient.risk_category}</span>
        </div>
        <h3>${patient.first_name} ${patient.last_name}</h3>
        <p>${patient.gender} · ${patient.region}</p>
        <dl>
          <div><dt>Risk</dt><dd>${patient.framingham_score}%</dd></div>
          <div><dt>ID</dt><dd>${patient.patient_id}</dd></div>
        </dl>
      </article>
    `).join("");
  });
}
