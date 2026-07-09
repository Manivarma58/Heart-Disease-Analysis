document.addEventListener("DOMContentLoaded", () => {
  const endpoint = "/api/visualizations-data";
  
  // Theme colors
  const primaryColor = "hsla(348, 83%, 47%, 0.85)"; // Heart disease red
  const primaryHoverColor = "hsla(348, 83%, 47%, 1.0)";
  const strokeColor = "hsla(198, 85%, 45%, 0.85)"; // Stroke blue
  const strokeHoverColor = "hsla(198, 85%, 45%, 1.0)";
  
  const colors = [
    "hsla(220, 15%, 55%, 0.6)",  // Grey
    "hsla(36, 100%, 50%, 0.75)",  // Amber
    "hsla(348, 83%, 47%, 0.8)",   // Red
    "hsla(150, 60%, 40%, 0.75)",  // Green
    "hsla(271, 70%, 50%, 0.75)",  // Purple
    "hsla(198, 85%, 45%, 0.75)",  // Light blue
  ];

  fetch(endpoint)
    .then(response => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })
    .then(data => {
      initCharts(data);
    })
    .catch(error => {
      console.error("Error loading visualization data:", error);
    });

  function initCharts(data) {
    // Shared chart options creator
    const getOptions = (titleY, rateLabel = "Prevalence Rate") => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              const row = context.raw;
              if (row && typeof row === "object" && "rate" in row) {
                return ` ${rateLabel}: ${row.rate}% (${row.cases} cases out of ${row.total} patients)`;
              }
              return ` ${context.dataset.label || ""}: ${context.parsed.y || context.parsed.x}%`;
            }
          }
        }
      },
      scales: {
        x: { grid: { color: "rgba(156, 163, 175, 0.1)" } },
        y: {
          title: { display: true, text: titleY, font: { size: 11 } },
          grid: { color: "rgba(156, 163, 175, 0.1)" },
          ticks: { callback: value => `${value}%` }
        }
      }
    });

    // 1. Gender vs Heart Disease
    const ctx1 = document.getElementById("chart-gender-hd").getContext("2d");
    const gData = data.gender_hd.map(r => ({
      x: r.sex,
      y: parseFloat(((r.cases / r.total) * 100).toFixed(2)),
      cases: r.cases,
      total: r.total,
      rate: ((r.cases / r.total) * 100).toFixed(2)
    }));
    new Chart(ctx1, {
      type: "bar",
      data: {
        datasets: [{
          data: gData,
          backgroundColor: [colors[0], primaryColor],
          hoverBackgroundColor: [colors[0], primaryHoverColor],
          borderRadius: 6
        }]
      },
      options: getOptions("Heart Disease Rate (%)")
    });

    // 2. Age vs Heart Disease
    const ctx2 = document.getElementById("chart-age-hd").getContext("2d");
    const ageData = data.age_hd.map(r => ({
      x: r.age_category,
      y: parseFloat(((r.cases / r.total) * 100).toFixed(2)),
      cases: r.cases,
      total: r.total,
      rate: ((r.cases / r.total) * 100).toFixed(2)
    }));
    new Chart(ctx2, {
      type: "line",
      data: {
        labels: data.age_hd.map(r => r.age_category),
        datasets: [{
          data: ageData,
          borderColor: primaryColor,
          backgroundColor: "rgba(239, 68, 68, 0.1)",
          fill: true,
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: primaryColor
        }]
      },
      options: {
        ...getOptions("Heart Disease Rate (%)"),
        plugins: {
          ...getOptions("Heart Disease Rate (%)").plugins,
          legend: { display: false }
        }
      }
    });

    // 3. Diabetic vs Stroke
    const ctx3 = document.getElementById("chart-diabetic-stroke").getContext("2d");
    const dStrokeData = data.diabetic_stroke.map(r => ({
      x: r.diabetic,
      y: parseFloat(((r.cases / r.total) * 100).toFixed(2)),
      cases: r.cases,
      total: r.total,
      rate: ((r.cases / r.total) * 100).toFixed(2)
    }));
    new Chart(ctx3, {
      type: "bar",
      data: {
        datasets: [{
          data: dStrokeData,
          backgroundColor: [colors[0], colors[1], strokeColor, colors[4]],
          borderRadius: 6
        }]
      },
      options: getOptions("Stroke Rate (%)", "Stroke Rate")
    });

    // 4. Impact of Smoking & Alcohol
    const ctx4 = document.getElementById("chart-smoking-alcohol").getContext("2d");
    const cohorts = [
      { label: "Neither", filter: r => r.smoking === "No" && r.alcohol_drinking === "No" },
      { label: "Alcohol Only", filter: r => r.smoking === "No" && r.alcohol_drinking === "Yes" },
      { label: "Smoking Only", filter: r => r.smoking === "Yes" && r.alcohol_drinking === "No" },
      { label: "Both", filter: r => r.smoking === "Yes" && r.alcohol_drinking === "Yes" }
    ];
    const saData = cohorts.map(c => {
      const found = data.smoking_alcohol.find(c.filter);
      const total = found ? found.total : 0;
      const cases = found ? found.cases : 0;
      const rate = total > 0 ? ((cases / total) * 100).toFixed(2) : "0.00";
      return {
        x: c.label,
        y: parseFloat(rate),
        cases: cases,
        total: total,
        rate: rate
      };
    });
    new Chart(ctx4, {
      type: "bar",
      data: {
        datasets: [{
          data: saData,
          backgroundColor: [colors[0], colors[5], colors[1], primaryColor],
          borderRadius: 6
        }]
      },
      options: getOptions("Heart Disease Rate (%)")
    });

    // 5. Other Diseases vs Stroke
    const ctx5 = document.getElementById("chart-other-diseases").getContext("2d");
    const odDataYes = [];
    const odDataNo = [];
    const odLabels = ["Asthma", "Kidney Disease", "Skin Cancer"];
    
    odLabels.forEach(label => {
      const yesRow = data.other_diseases.find(r => r.condition_name === label && r.status === "Yes");
      const noRow = data.other_diseases.find(r => r.condition_name === label && r.status === "No");
      
      const yesTotal = yesRow ? yesRow.total : 0;
      const yesCases = yesRow ? yesRow.cases : 0;
      const yesRate = yesTotal > 0 ? ((yesCases / yesTotal) * 100).toFixed(2) : "0.00";
      
      const noTotal = noRow ? noRow.total : 0;
      const noCases = noRow ? noRow.cases : 0;
      const noRate = noTotal > 0 ? ((noCases / noTotal) * 100).toFixed(2) : "0.00";
      
      odDataYes.push({
        x: label,
        y: parseFloat(yesRate),
        cases: yesCases,
        total: yesTotal,
        rate: yesRate
      });
      odDataNo.push({
        x: label,
        y: parseFloat(noRate),
        cases: noCases,
        total: noTotal,
        rate: noRate
      });
    });
    new Chart(ctx5, {
      type: "bar",
      data: {
        labels: odLabels,
        datasets: [
          {
            label: "Has Disease (Yes)",
            data: odDataYes,
            backgroundColor: strokeColor,
            borderRadius: 6
          },
          {
            label: "No Disease (No)",
            data: odDataNo,
            backgroundColor: colors[0],
            borderRadius: 6
          }
        ]
      },
      options: {
        ...getOptions("Stroke Rate (%)", "Stroke Rate"),
        plugins: {
          legend: { display: true, position: "top" },
          tooltip: {
            callbacks: {
              label: function(context) {
                const row = context.raw;
                return ` ${context.dataset.label}: ${row.rate}% (${row.cases} stroke cases / ${row.total})`;
              }
            }
          }
        }
      }
    });

    // 6. Race-wise Heart Disease
    const ctx6 = document.getElementById("chart-race-hd").getContext("2d");
    const raceLabels = data.race_hd.map(r => r.race);
    const rData = data.race_hd.map(r => ({
      y: r.race,
      x: parseFloat(((r.cases / r.total) * 100).toFixed(2)),
      cases: r.cases,
      total: r.total,
      rate: ((r.cases / r.total) * 100).toFixed(2)
    }));
    new Chart(ctx6, {
      type: "bar",
      data: {
        labels: raceLabels,
        datasets: [{
          data: rData,
          backgroundColor: colors.slice(0, raceLabels.length),
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function(context) {
                const row = context.raw;
                return ` Prevalence Rate: ${row.rate}% (${row.cases} cases out of ${row.total} patients)`;
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: "Heart Disease Rate (%)", font: { size: 11 } },
            ticks: { callback: value => `${value}%` },
            grid: { color: "rgba(156, 163, 175, 0.1)" }
          },
          y: { grid: { display: false } }
        }
      }
    });

    // 7. General Health vs Heart Disease
    const ctx7 = document.getElementById("chart-gen-health").getContext("2d");
    const ghData = data.gen_health_hd.map(r => ({
      x: r.gen_health,
      y: parseFloat(((r.cases / r.total) * 100).toFixed(2)),
      cases: r.cases,
      total: r.total,
      rate: ((r.cases / r.total) * 100).toFixed(2)
    }));
    new Chart(ctx7, {
      type: "bar",
      data: {
        datasets: [{
          data: ghData,
          backgroundColor: [primaryColor, colors[1], colors[0], colors[5], colors[3]],
          borderRadius: 6
        }]
      },
      options: getOptions("Heart Disease Rate (%)")
    });

    // 8. Physical Activity vs Heart Disease
    const ctx8 = document.getElementById("chart-activity-hd").getContext("2d");
    const actData = data.activity_hd.map(r => ({
      x: r.physical_activity === "Yes" ? "Physically Active (Yes)" : "Inactive (No)",
      y: parseFloat(((r.cases / r.total) * 100).toFixed(2)),
      cases: r.cases,
      total: r.total,
      rate: ((r.cases / r.total) * 100).toFixed(2)
    }));
    new Chart(ctx8, {
      type: "bar",
      data: {
        datasets: [{
          data: actData,
          backgroundColor: [colors[3], primaryColor],
          borderRadius: 6
        }]
      },
      options: getOptions("Heart Disease Rate (%)")
    });

    // 9. Age & BMI vs Diabetic (Scatter Plot)
    const ctx9 = document.getElementById("chart-age-bmi-diabetic").getContext("2d");
    const diabYes = data.age_bmi_diabetic.filter(r => r.diabetic !== "No").map(r => ({ x: r.age, y: r.bmi, cat: r.age_category }));
    const diabNo = data.age_bmi_diabetic.filter(r => r.diabetic === "No").map(r => ({ x: r.age, y: r.bmi, cat: r.age_category }));
    new Chart(ctx9, {
      type: "scatter",
      data: {
        datasets: [
          {
            label: "Diabetic (Yes/Borderline)",
            data: diabYes,
            backgroundColor: "rgba(245, 158, 11, 0.8)", // Orange amber
            pointRadius: 5
          },
          {
            label: "Non-Diabetic (No)",
            data: diabNo,
            backgroundColor: "rgba(156, 163, 175, 0.6)", // Gray
            pointRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: true, position: "top" },
          tooltip: {
            callbacks: {
              label: function(context) {
                const pt = context.raw;
                return ` ${context.dataset.label}: Age range ${pt.cat}, BMI ${pt.y}`;
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: "Age Midpoint (Years)" },
            grid: { color: "rgba(156, 163, 175, 0.1)" }
          },
          y: {
            title: { display: true, text: "BMI" },
            grid: { color: "rgba(156, 163, 175, 0.1)" }
          }
        }
      }
    });

    // 10. Stroke Cohort Overlap
    const ctx10 = document.getElementById("chart-stroke-overlap").getContext("2d");
    const soData = data.stroke_overlap.map(r => ({
      x: r.cohort,
      y: parseFloat(((r.cases / r.total) * 100).toFixed(2)),
      cases: r.cases,
      total: r.total,
      rate: ((r.cases / r.total) * 100).toFixed(2)
    }));
    new Chart(ctx10, {
      type: "bar",
      data: {
        datasets: [{
          data: soData,
          backgroundColor: [colors[0], colors[5], colors[1], strokeColor],
          borderRadius: 6
        }]
      },
      options: getOptions("Stroke Rate (%)", "Stroke Rate")
    });
  }
});
