
function validateForm() {
  // Phone Number Validation
  var phone = document.getElementById("phone").value;
  var phonePattern = /^(\+977)?[0-9]{10}$/;
  var phoneError = document.getElementById("phone-error");
  if (!phone.match(phonePattern)) {
    phoneError.innerHTML = "Please enter a valid phone number (10 digits).";
    return false;
  } else {
    phoneError.innerHTML = "";
  }

  // Password Validation (minimum 8 characters)
  var password = document.getElementById("password").value;
  var confirmPassword = document.getElementById("confirm_password").value;
  var passwordError = document.getElementById("password-error");
  if (password.length < 8) {
    passwordError.innerHTML =
      "Password must be at least 8 characters long.";
    return false;
  } else if (password !== confirmPassword) {
    passwordError.innerHTML = "Passwords do not match.";
    return false;
  } else {
    passwordError.innerHTML = "";
  }

  return true;
}
