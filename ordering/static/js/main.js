window.addEventListener("scroll", function () {

    const nav = document.querySelector(".glass-navbar");

    if (window.scrollY > 80) {

        nav.style.background = "rgba(7,19,32,.92)";

        nav.style.padding = "12px 0";

    }

    else {

        nav.style.background = "rgba(7,19,32,.55)";

        nav.style.padding = "18px 0";

    }

});

/* CATEGORY FILTER */

function filterMenu(category) {

    const items = document.querySelectorAll(".menu-item");

    const buttons = document.querySelectorAll(".filter-btn");

    buttons.forEach(btn => btn.classList.remove("active"));

    event.target.classList.add("active");

    items.forEach(item => {

        if (category === "all") {

            item.classList.remove("hidden");

        }

        else if (item.dataset.category === category) {

            item.classList.remove("hidden");

        }

        else {

            item.classList.add("hidden");

        }

    });

}

const search = document.getElementById("menuSearch");

if (search) {

    search.addEventListener("keyup", function () {

        const value = this.value.toLowerCase();

        document.querySelectorAll(".food-card, .menu-card").forEach(card => {

            const text = card.innerText.toLowerCase();

            const col = card.closest(".col-lg-3");

            if (col) {

                col.style.display =

                    text.includes(value)

                        ?

                        "block"

                        :

                        "none";

            }

        });

    });

}


/* Scroll To Top */

const scrollBtn = document.getElementById("scrollTopBtn");

if (scrollBtn) {

    scrollBtn.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}


/* ==========================================
      Category Showcase Rotating Circle
========================================== */

const categoryShowcaseItems = [
    { name: "Pizza", image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=900" },
    { name: "Burger", image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=900" },
    { name: "Pasta", image: "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=900" },
    { name: "Desserts", image: "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=900" },
    { name: "Drinks", image: "https://images.unsplash.com/photo-1497534446932-c925b458314e?w=900" }
];

let currentShowcaseIndex = 0;

function rotateCategoryShowcase() {
    const imgEl = document.getElementById("showcaseImage");
    const labelEl = document.getElementById("showcaseLabel");
    if (!imgEl || !labelEl) return;

    currentShowcaseIndex = (currentShowcaseIndex + 1) % categoryShowcaseItems.length;
    const nextItem = categoryShowcaseItems[currentShowcaseIndex];

    // Fade and rotate out
    imgEl.classList.add("fade-out");
    labelEl.classList.add("fade-out");

    setTimeout(() => {
        // Swap sources
        imgEl.src = nextItem.image;
        imgEl.alt = nextItem.name;
        labelEl.innerText = nextItem.name;

        // Trigger fade/rotate in
        imgEl.classList.remove("fade-out");
        labelEl.classList.remove("fade-out");
    }, 800);
}

function startCategoryShowcase() {
    const imgEl = document.getElementById("showcaseImage");
    if (imgEl) {
        setInterval(rotateCategoryShowcase, 4000);
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startCategoryShowcase);
} else {
    startCategoryShowcase();
}

function scrollToSearch() {
    const searchEl = document.getElementById("menuSearch");
    if (searchEl) {
        searchEl.scrollIntoView({ behavior: "smooth" });
        searchEl.focus();
    } else {
        window.location = "/#menu";
    }
}

function triggerSearch() {
    const searchEl = document.getElementById("menuSearch");
    if (searchEl) {
        const event = new Event("keyup");
        searchEl.dispatchEvent(event);
        const menuEl = document.getElementById("menu");
        if (menuEl) {
            menuEl.scrollIntoView({ behavior: "smooth" });
        }
    }
}