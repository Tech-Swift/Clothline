function handleAddToCart(itemId) {
    fetch('/check-login-status/')
        .then(response => response.json())
        .then(data => {
            if (data.is_authenticated) {
                addToCart(itemId); // Call add to cart if logged in
            } else {
                alert("You must be logged in to add items to the cart.");
                window.location.href = '/login/';  // Optionally redirect to login
            }
        })
        .catch(error => console.error("Error:", error));
}

function addToCart(itemId) {
    fetch(`/add-to-cart/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            updateCartCount(data.cart_count);
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while adding to the cart.");
    });
}
function updateCartCount(count) {
    document.getElementById("cart-count").textContent = count;
}
