document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("doctor-container");

  DoctorData.forEach((doc) => {
    const card = document.createElement("div");
    card.classList.add("doctor-card");

    card.innerHTML = `
      <img src="${doc.image}" alt="${doc.name}" class="doctor-image" />
      <h2>${doc.name}</h2>
      <p><strong>Specialist:</strong> ${doc.specialist}</p>
      <p><strong>Department:</strong> ${doc.dept}</p>
      <p><strong>Visiting Hour:</strong> ${doc.hour}</p>
      <p class="visit-fee"><strong>Visit Fee:</strong> ${doc.visit}</p>
    `;

    container.appendChild(card);
  });
});
