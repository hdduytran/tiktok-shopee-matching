function clickUntilDisabled(buttonId) {
    const interval = setInterval(() => {
        const button = document.querySelector(buttonId);

        if (button && !button.disabled) {
            button.click();
        } else {
            clearInterval(interval);
            console.log('Button is no longer clickable.');
        }
    }, 1000); // Clicks every 1000 milliseconds (1 second)
}

// Usage: Replace 'yourButtonId' with the actual ID of the button.
clickUntilDisabled("#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div > fieldset > div.shopee-mini-page-controller > button.shopee-button-outline.shopee-mini-page-controller__next-btn");
clickUntilDisabled("#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.container > div.shop-page__all-products-section > div.shop-page_product-list > div.shop-sold-out-items-view > div > div.shopee-header-section__content > div.shop-sold-out-see-more > button");