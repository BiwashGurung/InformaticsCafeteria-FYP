function increaseQuantity(button) {
    let inputField = button.previousElementSibling;
    let currentValue = parseInt(inputField.value, 10);
    inputField.value = currentValue + 1;
}

function decreaseQuantity(button) {
    let inputField = button.nextElementSibling;
    let currentValue = parseInt(inputField.value, 10);
    if (currentValue > 1) {
        inputField.value = currentValue - 1;
    }
}



