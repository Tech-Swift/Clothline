document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".cart-btn").forEach(button => {
        button.addEventListener("click", function () {
            let itemId = this.getAttribute("data-item-id");
            
            fetch("/add-to-cart/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ item_id: itemId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById("cart-count").innerText = data.cart_count;
                    alert("Item added to cart!");
                } else {
                    alert(data.error);
                }
            });
        });
    });

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
