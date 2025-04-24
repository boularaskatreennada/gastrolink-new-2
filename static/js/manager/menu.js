const menuItems = [
    { id: 1, name: 'Caesar Salad', price: 10, img: STATIC_URL + 'images/cesar salad.jpg' },
    { id: 2, name: 'Cobb Salad', price: 15, img: STATIC_URL + 'images/cobb salad.jpg' },
  ];
  const menuList = document.getElementById('menu-list');
  const orderList = document.getElementById('order-list');
  const totalPriceSpan = document.getElementById('total-price');

  const orders = {}; // Object to track items in order

  // Render each menu item
  menuItems.forEach(item => {
    const div = document.createElement('div');
    div.className = 'd-flex justify-content-between align-items-center border-bottom py-2';

    div.innerHTML = `
      <img src="${item.img}" alt="${item.name}" class="menu-img mr-3">
      <div class=""><strong>${item.name}</strong></div>
      <div class="input-group w-25">
        <input type="number" min="1" value="1" class="form-control quantity" id="qty-${item.id}">
        <div class="input-group-append">
          <button class="btn add-btn" 
                  data-id="${item.id}" 
                  data-name="${item.name}" 
                  data-price="${item.price}">
            Add
          </button>
        </div>
      </div>
    `;
    menuList.appendChild(div);
  });

  // Handle button clicks
  document.addEventListener('click', function (e) {
    // Add button clicked
    if (e.target.classList.contains('add-btn')) {
      const id = e.target.dataset.id;
      const name = e.target.dataset.name;
      const price = parseFloat(e.target.dataset.price);
      const qty = parseInt(document.getElementById(`qty-${id}`).value);

      if (qty > 0) {
        // Update quantity if item already exists
        if (orders[id]) {
          orders[id].quantity += qty;
        } else {
          orders[id] = { name, price, quantity: qty };
        }
        renderOrderList();
      }
    }

    // Remove button clicked
    if (e.target.classList.contains('remove-btn')) {
      const itemId = e.target.dataset.id;
      delete orders[itemId];
      renderOrderList();
    }
  });

  // Update the order list UI and total
  function renderOrderList() {
    orderList.innerHTML = '';

    for (let id in orders) {
      const item = orders[id];
      const li = document.createElement('li');
      li.className = 'list-group-item d-flex justify-content-between align-items-center';

      li.innerHTML = `
        ${item.name}
        <span>$${item.price} x ${item.quantity}</span>
        <button class="remove-btn ml-3" data-id="${id}">&times;</button>
      `;

      orderList.appendChild(li);
     
    }
}

  document.getElementById('toggle-order-box').addEventListener('click', function () {
    document.getElementById('order-box-overlay').classList.add('show');
  });

  document.getElementById('close-order-box').addEventListener('click', function () {
    document.getElementById('order-box-overlay').classList.remove('show');
  });

  // Optional: Sync order list content (copy innerHTML from original)
  function syncOrderList() {
    document.getElementById('order-list-overlay').innerHTML = document.getElementById('order-list').innerHTML;
  }

  // Sync when opening overlay
  document.getElementById('toggle-order-box').addEventListener('click', syncOrderList);

