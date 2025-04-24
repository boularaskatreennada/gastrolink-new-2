new DataTable('#plats-table');
new DataTable('#ingredients-table');

document.addEventListener("DOMContentLoaded", function () {
    const platsBtn = document.getElementById("plats-btn");
    const ingredientsBtn = document.getElementById("ingredients-btn");
    const platsTable = document.getElementById("plats");
    const ingredientsTable = document.getElementById("ingredients");

    // Fonction pour mettre à jour le style actif
    function updateActiveHeader(activeBtn, inactiveBtn) {
        activeBtn.style.color = "#FA4516";
        activeBtn.style.borderBottom = "2px solid #FA4516";
        activeBtn.style.fontWeight = "600";
        inactiveBtn.style.color = "#000";
        inactiveBtn.style.borderBottom = "none";
        inactiveBtn.style.fontWeight = "normal";
    }

    // Affichage par défaut : Plats
    platsTable.classList.remove("d-none");
    ingredientsTable.classList.add("d-none");
    updateActiveHeader(platsBtn, ingredientsBtn);

    platsBtn.addEventListener("click", function () {
        platsTable.classList.remove("d-none");
        ingredientsTable.classList.add("d-none");
        updateActiveHeader(platsBtn, ingredientsBtn);
    });

    ingredientsBtn.addEventListener("click", function () {
        ingredientsTable.classList.remove("d-none");
        platsTable.classList.add("d-none");
        updateActiveHeader(ingredientsBtn, platsBtn);
    });
});
