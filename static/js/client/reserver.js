
function selectRestaurant(element, restaurantId) {
    const cards = document.querySelectorAll('.restaurant-card');
    cards.forEach(card => card.classList.remove('active'));
    element.classList.add('active');

    document.querySelectorAll('.table-plan').forEach(img => img.classList.remove('active'));
    document.getElementById(restaurantId + '-plan').classList.add('active');
    updateTableSelect(restaurantId);
}

function updateTableSelect(restaurantId) {
    const tableSelect = document.getElementById('table');
    tableSelect.innerHTML = '';
    const tables = getAvailableTables(restaurantId);
    tables.forEach(table => {
        const option = document.createElement('option');
        option.value = table;
        option.innerText = `Table ${table}`;
        tableSelect.appendChild(option);
    });
}

function getAvailableTables(restaurantId) {
    const tables = {
        'ali-mendjeli': [1, 2, 3, 4],
        'el-khroub': [1, 2, 3],
        'centre-ville': [1, 2, 3, 4, 5],
        'aeroport': [1, 2]
    };
    return tables[restaurantId] || [];
}

document.getElementById('reservation-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const client_name = document.getElementById('clientName').value;
    const phone = document.getElementById('phone').value;
    const restaurant_id = document.getElementById('restaurant').value;
    const table_number = document.getElementById('table').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const datetime = `${date}T${time}:00`;
    const duration = document.getElementById('duration').value;
    const number_of_people = document.getElementById('number_of_people').value;

    if (!client_name || !phone || !restaurant_id || !table_number || !date || !time || !duration || !number_of_people) {
        alert('Merci de remplir tous les champs.');
        return;
    }

    const reservationData = {
        client_name: client_name,
        phone: phone,
        restaurant_id: restaurant_id,
        table_number: table_number,
        datetime: datetime,
        duration: duration,
        number_of_people: number_of_people
    };

    fetch('/reservations/reserver_table/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify(reservationData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Réservation confirmée !');
        } else {
            alert(data.message || 'Erreur lors de la réservation.');
        }
    })
    .catch(error => {
        alert('Erreur réseau : ' + error);
    });
});
