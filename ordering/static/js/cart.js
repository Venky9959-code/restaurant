/* ==========================================
        DineFlow Shopping Cart
========================================== */

let cart = JSON.parse(localStorage.getItem("cart")) || [];

/* Save Cart */

function saveCart() {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

}

/* Toggle Sidebar */

function toggleCart() {

    document
        .getElementById("cartSidebar")
        .classList.toggle("open");

}

/* Add Item */

function addToCart(id, name, price, image) {

    let item = cart.find(product => product.id == id);

    if (item) {

        item.quantity++;

    }

    else {

        cart.push({

            id: id,

            name: name,

            price: Number(price),

            image: image,

            quantity: 1

        });

    }

    saveCart();

    updateCart();

    showToast(name + " added to cart");

}


/* Update Cart */

function updateCart() {

    let cartItems = document.getElementById("cartItems");

    let badge = document.getElementById("cartBadge");

    cartItems.innerHTML = "";

    let subtotal = 0;

    cart.forEach(item => {

        subtotal += item.price * item.quantity;

        cartItems.innerHTML += `

<div class="cart-product">

<img src="${item.image}">

<div class="cart-info">

<h6>${item.name}</h6>

<p>₹${item.price}</p>

</div>

<div class="qty-box">

<button onclick="changeQty('${item.id}',-1)">

-

</button>

<span>

${item.quantity}

</span>

<button onclick="changeQty('${item.id}',1)">

+

</button>

</div>

</div>

`;

    });

    let gst = subtotal * 0.05;

    let total = subtotal + gst;

    document.getElementById("subtotal").innerText = subtotal.toFixed(2);

    document.getElementById("gst").innerText = gst.toFixed(2);

    document.getElementById("grandTotal").innerText = total.toFixed(2);

    badge.innerText = cart.length;

    saveCart();

}



/* Quantity */

function changeQty(id, value) {

    cart = cart.map(item => {

        if (item.id == id) {

            item.quantity += value;

        }

        return item;

    }).filter(item => item.quantity > 0);

    updateCart();

}

/* Clear */

function clearCart() {

    cart = [];

    updateCart();

}




/* Toast */

function showToast(message) {

    let toast = document.createElement("div");

    toast.className = "toast-msg";

    toast.innerHTML = `

<i class="bi bi-check-circle-fill"></i>

${message}

`;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.remove();

    }, 3000);

}

/* Initial */

updateCart();


async function submitOrder() {

    const name = document.querySelector(
        "[name='customer_name']"
    ).value;

    const phone = document.querySelector(
        "[name='customer_phone']"
    ).value;

    const table = document.querySelector(
        "[name='table_number']"
    ).value;

    const paymentMethodEl = document.querySelector(
        "[name='payment_method']:checked"
    );
    const payment_method = paymentMethodEl ? paymentMethodEl.value : "COD";

    const total = parseFloat(

        document.getElementById(
            "grandTotal"
        ).innerText

    );

    if (payment_method === "ONLINE") {
        var options = {
            "key": "rzp_test_dummykey12345",
            "amount": Math.round(total * 100),
            "currency": "INR",
            "name": "DineFlow AI",
            "description": "Smart Restaurant Order",
            "image": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/cup-hot-fill.svg",
            "handler": async function (response) {
                const orderResponse = await fetch("/place-order/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({
                        customer: { name, phone, table, total, payment_method: "ONLINE" },
                        cart
                    })
                });
                const result = await orderResponse.json();
                if (result.success) {
                    localStorage.removeItem("cart");
                    window.location = "/success/" + result.order_id + "/";
                }
            },
            "prefill": {
                "name": name,
                "contact": phone
            },
            "theme": {
                "color": "#ff7a00"
            }
        };
        var rzp = new Razorpay(options);
        rzp.open();
    } else {
        const response = await fetch(

            "/place-order/",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                    "X-CSRFToken": getCookie("csrftoken")

                },

                body: JSON.stringify({

                    customer: {

                        name,

                        phone,

                        table,

                        total,

                        payment_method: "COD"

                    },

                    cart

                })

            }

        );

        const result = await response.json();

        if (result.success) {

            localStorage.removeItem("cart");

            window.location = "/success/" + result.order_id + "/";

        }
    }
}


function getCookie(name) {

    let cookieValue = null;

    if (document.cookie) {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(

                    cookie.substring(name.length + 1)

                );

            }

        }

    }

    return cookieValue;

}


function goToCheckout() {

    window.location = "/checkout/";

}


/* ==========================================
        DineFlow Wishlist Functionality
========================================== */

let wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];

function saveWishlist() {
    localStorage.setItem("wishlist", JSON.stringify(wishlist));
}

function toggleWishlist(id, name) {
    const index = wishlist.indexOf(id);
    if (index > -1) {
        wishlist.splice(index, 1);
        showToast(name + " removed from wishlist");
    } else {
        wishlist.push(id);
        showToast(name + " added to wishlist");
    }
    saveWishlist();
    updateWishlistUI();
}

function updateWishlistUI() {
    // Update profile count if tag exists
    const profileCount = document.getElementById("profileWishlistCount");
    if (profileCount) {
        profileCount.innerText = wishlist.length;
    }

    // Toggle filled heart states on all card wishlist buttons matching IDs
    document.querySelectorAll(".wishlist-btn").forEach(btn => {
        const itemId = btn.getAttribute("data-item-id");
        const icon = btn.querySelector("i");
        if (itemId && icon) {
            if (wishlist.includes(itemId)) {
                icon.className = "bi bi-heart-fill text-danger";
            } else {
                icon.className = "bi bi-heart";
            }
        }
    });
}

function reorder(items) {
    items.forEach(item => {
        let cartItem = cart.find(product => product.id == item.id);
        if (cartItem) {
            cartItem.quantity += item.quantity;
        } else {
            cart.push({
                id: item.id,
                name: item.name,
                price: Number(item.price),
                image: item.image,
                quantity: item.quantity
            });
        }
    });
    saveCart();
    updateCart();
    document.getElementById("cartSidebar").classList.add("open");
    showToast("Reordered items added to cart!");
}

// Perform initial UI sync once page elements load
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", updateWishlistUI);
} else {
    updateWishlistUI();
}



