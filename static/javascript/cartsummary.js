// Cart Summary Page JavaScript
    const orderForm = document.getElementById('orderForm');
    const khaltiModal = document.getElementById('khaltiModal');
    const onlinePayment = document.getElementById('onlinePayment');
    const cashPayment = document.getElementById('cashPayment');
    const pickupOption = document.getElementById('pickupOption');
    const dineInOption = document.getElementById('dineInOption');
    const pickupTimeDiv = document.getElementById('pickupTime');
    const dineInTimeDiv = document.getElementById('dineInTime');
    const pickupTimeInput = pickupTimeDiv.querySelector('input[name="pickup_time"]');
    const dineInTimeInput = dineInTimeDiv.querySelector('input[name="dine_in_time"]');
    const orderButton = document.getElementById('orderButton');

    // Show/hide time inputs based on radio selection
    function toggleTimeInputs() {
        if (pickupOption.checked) {
            pickupTimeDiv.style.display = 'block';
            dineInTimeDiv.style.display = 'none';
            dineInTimeInput.value = '';
        } else if (dineInOption.checked) {
            pickupTimeDiv.style.display = 'none';
            dineInTimeDiv.style.display = 'block';
            pickupTimeInput.value = '';
        }
    }

    // Initial state
    toggleTimeInputs();

    // Event listeners for radio buttons
    pickupOption.addEventListener('change', toggleTimeInputs);
    dineInOption.addEventListener('change', toggleTimeInputs);

    // Sync Khalti form fields on submit
    if (khaltiModal) {
        const khaltiForm = document.getElementById('khaltiForm');
        khaltiForm.addEventListener('submit', function() {
            const remarks = document.getElementById('remarks').value;
            document.getElementById('khaltiRemarks').value = remarks;
            if (pickupOption.checked) {
                document.getElementById('khaltiPickupTime').value = pickupTimeInput.value;
                document.getElementById('khaltiDineInTime').value = '';
            } else if (dineInOption.checked) {
                document.getElementById('khaltiPickupTime').value = '';
                document.getElementById('khaltiDineInTime').value = dineInTimeInput.value;
            }
        });

        // Reset to Cash when modal is closed
        khaltiModal.addEventListener('hidden.bs.modal', function() {
            cashPayment.checked = true;
            onlinePayment.checked = false;
            orderButton.style.display = 'block';
        });
    }

    // Prevent order form submission when Online Payment is selected
    orderForm.addEventListener('submit', function(e) {
        if (onlinePayment.checked) {
            e.preventDefault();
        }
    });
