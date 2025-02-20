function decreaseQuantity(button) {
    let input = button.nextElementSibling;
    let value = parseInt(input.value);
    if (value > 1) {
        input.value = value - 1;
    }
}

function increaseQuantity(button) {
    let input = button.previousElementSibling;
    let value = parseInt(input.value);
    input.value = value + 1;
}