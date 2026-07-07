function filterMenu(category, button) {

    document.querySelectorAll(".filter-btn")
        .forEach(btn => btn.classList.remove("active"));

    button.classList.add("active");

    document.querySelectorAll(".menu-item")
        .forEach(item => {

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