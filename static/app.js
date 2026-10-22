document.addEventListener("DOMContentLoaded", function () {
    var chips = document.querySelectorAll(".chip");
    var cards = document.querySelectorAll(".experience");

    chips.forEach(function (chip) {
        chip.addEventListener("click", function () {
            chips.forEach(function (c) { c.classList.remove("active"); });
            chip.classList.add("active");

            var filter = chip.dataset.filter;
            cards.forEach(function (card) {
                card.hidden = !(filter === "all" || card.dataset.outcome === filter);
            });
        });
    });
});