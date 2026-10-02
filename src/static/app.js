const loadButton = document.querySelector(
    '[data-testid="load-button"]'
);

const itemsCount = document.querySelector(
    '[data-testid="items-count"]'
);

const firstItemTitle = document.querySelector(
    '[data-testid="first-item-title"]'
);


loadButton.addEventListener("click", async () => {
    try {
        const response = await fetch("/api/v1/items");

        if (!response.ok) {
            itemsCount.textContent = "Error";
            firstItemTitle.textContent = "Unable to load items";
            return;
        }

        const result = await response.json();

        const items = result.data;

        itemsCount.textContent = items.length;

        if (items.length === 0) {
            firstItemTitle.textContent = "No items";
        } else {
            firstItemTitle.textContent = items[0].title;
        }

    } catch (error) {
        itemsCount.textContent = "Error";
        firstItemTitle.textContent = "Unable to load items";
    }
});