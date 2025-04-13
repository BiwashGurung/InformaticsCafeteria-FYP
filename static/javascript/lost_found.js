// Lost and Found Form Validation and Animation
    document.getElementById('lostForm').addEventListener('submit', function(event) {
        const inputs = this.querySelectorAll('input[required], textarea[required]');
        let valid = true;
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                valid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        if (!valid) event.preventDefault();
    });

    document.querySelector('#lostForm button[type="submit"]').addEventListener('click', function(e) {
        if (this.form.checkValidity()) {
            this.querySelector('span:nth-child(2)').style.transform = 'scaleX(1)';
            setTimeout(() => this.querySelector('span:nth-child(2)').style.transform = 'scaleX(0)', 500);
        }
    });
