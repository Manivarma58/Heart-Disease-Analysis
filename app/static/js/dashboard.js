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
        <p>${patient.age} yrs · ${patient.gender} · ${patient.region}</p>
        <dl>
          <div><dt>Risk</dt><dd>${patient.framingham_score}%</dd></div>
          <div><dt>BP</dt><dd>${patient.systolic_bp}</dd></div>
          <div><dt>Chol.</dt><dd>${patient.cholesterol_total}</dd></div>
          <div><dt>BMI</dt><dd>${patient.bmi}</dd></div>
        </dl>
        <p class="recommendation">${patient.recommendation}</p>
      </article>
    `).join("");
  });
}
