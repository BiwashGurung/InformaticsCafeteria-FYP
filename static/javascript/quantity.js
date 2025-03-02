document.querySelectorAll(".add-to-cart-form").forEach(form => {
    form.addEventListener("submit", function(event) {
        let quantityInput = this.querySelector(".quantity-input");
        let quantityValue = parseInt(quantityInput.value);

        if (!quantityValue || quantityValue < 1) {
            // Preventing the form submission if quantity is invalid
            event.preventDefault(); 
            alert("Quantity must be at least 1.");
            // Resetting to minimum valid value
            quantityInput.value = 1; 
        }
    });
});
