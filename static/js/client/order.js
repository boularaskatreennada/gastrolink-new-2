
document.addEventListener('DOMContentLoaded', function() {
    // Gestion du panier
    let cart = [];
    
    // Sélection des éléments du DOM
    const orderItemsEl = document.querySelector('.order-items');
    const orderCountEl = document.querySelector('.order-count');
    const orderTotalEl = document.querySelector('.order-total span:last-child');
    const submitBtn = document.querySelector('.submit-btn');
    const orderSummary = document.querySelector('.order-summary');
    const cartToggle = document.querySelector('.cart-toggle');
    const cartBadge = document.querySelector('.cart-badge');
    
    // Fonction pour mettre à jour l'affichage du panier
    function updateCartDisplay() {
        if (cart.length === 0) {
            orderItemsEl.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
            orderCountEl.textContent = '0';
            cartBadge.textContent = '0';
            orderTotalEl.textContent = '0 $';
            submitBtn.disabled = true;
            return;
        }
        
        let itemsHtml = '';
        let total = 0;
        let totalItems = 0;
        
        cart.forEach(item => {
            itemsHtml += `
                <div class="order-item" data-id="${item.id}">
                    <span>${item.name}</span>
                    <div class="order-item-controls">
                        <span>${item.quantity} x ${item.price} $</span>
                        <button class="order-item-btn minus">-</button>
                        <button class="order-item-btn plus">+</button>
                        <button class="order-item-btn remove">×</button>
                    </div>
                </div>
            `;
            total += item.quantity * item.price;
            totalItems += item.quantity;
        });
        
        orderItemsEl.innerHTML = itemsHtml;
        orderCountEl.textContent = totalItems;
        cartBadge.textContent = totalItems;
        orderTotalEl.textContent = `${total} $`;
        submitBtn.disabled = false;
        
        // Ajout des écouteurs d'événements pour les boutons de contrôle
        document.querySelectorAll('.order-item-btn.minus').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = parseInt(this.closest('.order-item').getAttribute('data-id'));
                updateItemQuantity(itemId, -1);
            });
        });
        
        document.querySelectorAll('.order-item-btn.plus').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = parseInt(this.closest('.order-item').getAttribute('data-id'));
                updateItemQuantity(itemId, 1);
            });
        });
        
        document.querySelectorAll('.order-item-btn.remove').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = parseInt(this.closest('.order-item').getAttribute('data-id'));
                removeItemFromCart(itemId);
            });
        });
    }
    
    // Fonction pour ajouter un article au panier
    function addToCart(itemId, itemName, itemPrice) {
        const existingItem = cart.find(item => item.id === itemId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                id: itemId,
                name: itemName,
                price: itemPrice,
                quantity: 1
            });
        }
        
        updateCartDisplay();
        
        // Sur mobile, ouvrir le panier quand on ajoute un article
        if (window.innerWidth <= 992) {
            orderSummary.classList.add('open');
        }
    }
    
    // Fonction pour mettre à jour la quantité d'un article
    function updateItemQuantity(itemId, change) {
        const item = cart.find(item => item.id === itemId);
        
        if (item) {
            item.quantity += change;
            
            if (item.quantity <= 0) {
                removeItemFromCart(itemId);
            } else {
                updateCartDisplay();
            }
        }
    }
    
    // Fonction pour supprimer un article du panier
    function removeItemFromCart(itemId) {
        cart = cart.filter(item => item.id !== itemId);
        updateCartDisplay();
    }
    
    // Fonction pour passer la commande
    function submitOrder() {
      
const note = document.querySelector('.order-note').value;

const orderData = {
client_id: 1, // à remplacer dynamiquement

restaurant_id: 1, // à remplacer dynamiquement
items: cart,
note: note,
total: cart.reduce((sum, item) => sum + (item.quantity * item.price), 0)
};

// Stocker les infos dans localStorage
localStorage.setItem('orderData', JSON.stringify(orderData));

// Rediriger vers la page de confirmation
window.location.href = "/client/confirm_order/";

    }
    
    // Écouteurs d'événements
    document.querySelectorAll('.add-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const itemId = parseInt(this.getAttribute('data-id'));
            const itemName = this.getAttribute('data-name');
            const itemPrice = parseInt(this.getAttribute('data-price'));
            addToCart(itemId, itemName, itemPrice);
        });
    });
    
    submitBtn.addEventListener('click', submitOrder);
    
    // Toggle pour afficher/masquer le panier sur mobile
    cartToggle.addEventListener('click', function() {
        orderSummary.classList.toggle('open');
    });
    
    // Fermer le panier quand on clique à l'extérieur (sur mobile)
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 992 && 
            !orderSummary.contains(e.target) && 
            !cartToggle.contains(e.target) &&
            orderSummary.classList.contains('open')) {
            orderSummary.classList.remove('open');
        }
    });
    
    // Gestion du changement de restaurant
    const restaurantSelect = document.querySelector('.restaurant-select');
    const addressDisplay = document.querySelector('.restaurant-address');

    const restaurantAddresses = {
        "Ali Mendjli, Constantine": "123 Rue Ali Mendjli, Constantine",
        "Centre Ville, Constantine": "45 Avenue de la République, Constantine",
        "Ibn Badis, Constantine": "12 Rue Ibn Badis, Constantine",
        "El Khroub": "Place Principale, El Khroub",
        "Aéroport Mohamed Boudiaf": "Zone Aéroportuaire, Constantine"
    };

    if (restaurantSelect && addressDisplay) {
        restaurantSelect.addEventListener('change', function() {
            const selectedRestaurant = this.value;
            addressDisplay.textContent = restaurantAddresses[selectedRestaurant] || "Adresse non disponible";
        });
    }
    
    // Initialiser l'affichage du panier
    updateCartDisplay();
    
    // Gestion du redimensionnement de la fenêtre
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            orderSummary.classList.remove('open');
        }
    });
});
