function togglePasswordVisibility(id) {
    const passwordInput = document.getElementById(id);
    const icon = passwordInput.nextElementSibling.querySelector('i');
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = "password";
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

document.querySelectorAll('.dropdown-menu .wallet-option').forEach(item => {
    item.addEventListener('click', function (event) {
        event.preventDefault();
        const value = this.getAttribute('data-value');
        const iconSrc = this.getAttribute('data-icon-src');
        const text = this.textContent.trim();
        document.getElementById('selectedWalletIcon').src = iconSrc;
        document.getElementById('selectedWalletText').textContent = text;
        document.getElementById('walletTypeHidden').value = value;
    });
});