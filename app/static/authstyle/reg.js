const togglePasswordButtons = document.querySelectorAll('.toggle-password');
const referralCode = document.getElementById("ref_code_tag");
const currentUrl = window.location.href;
if (currentUrl.includes('ref')) {
    let rCode = currentUrl.split('?')[1].split("=")[1];
    if (referralCode.value === "") {
        referralCode.value = rCode;
        referralCode.readOnly = true;
        referralCode.disable = true;
    }
}
togglePasswordButtons.forEach(button => {
    button.addEventListener('click', function () {
        const targetInputId = this.getAttribute('data-target');
        const passwordInput = document.getElementById(targetInputId);
        const eyeIcon = this.querySelector('i');
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            eyeIcon.classList.remove('fa-eye');
            eyeIcon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            eyeIcon.classList.remove('fa-eye-slash');
            eyeIcon.classList.add('fa-eye');
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    if (window.location.href.includes('auth/register')) {
        const walletTypeDropdownToggle = document.getElementById('walletTypeDropdownToggle');
        const selectedWalletTypeText = document.getElementById('selectedWalletTypeText');
        const walletTypeHiddenInput = document.getElementById('walletTypeHiddenInput');
        const dropdownMenuItems = document.querySelectorAll('.dropdown-item');
        function setSelectedWallet(value, text) {
            selectedWalletTypeText.textContent = text;
            walletTypeHiddenInput.value = value;
            dropdownMenuItems.forEach(item => item.classList.remove('active'));
            const selectedItem = document.querySelector(`#walletTypeDropdownToggle + .dropdown-menu .dropdown-item[data-value="${value}"]`);
            if (selectedItem) {
                selectedItem.classList.add('active');
            }
        }
        dropdownMenuItems.forEach(item => {
            item.addEventListener('click', function (event) {
                event.preventDefault();
                const selectedValue = this.getAttribute('data-value');
                const selectedText = this.textContent.trim();
                setSelectedWallet(selectedValue, selectedText);
            });
        });
        if (walletTypeHiddenInput.value) {
            setSelectedWallet(walletTypeHiddenInput.value, walletTypeHiddenInput.value);
        }
    }
    if (!window.location.href.includes("auth/terms-and-privacy-policy")) {
        const leftNotificationContainer = document.getElementById('leftNotificationContainer');
        function showLeftNotification(message, duration = 7000) {
            const notificationBox = leftNotificationContainer.querySelector('.left-notification-box');
            notificationBox.innerHTML = `${message}`;
            leftNotificationContainer.classList.add('show');
            setTimeout(() => {
                leftNotificationContainer.classList.remove('show');
            }, duration);
            }
            
        }
        const reciver = document.getElementById('reciver');
        if (reciver.textContent.trim()) {
            console.log("1", reciver.textContent)
            showLeftNotification(reciver.textContent);
            reciver.textContent = "";
        }
        // if (window.location.href.includes('auth/login')) {
        //     showLeftNotification(`Wlecome please fill the form to login`);
            
        // }
        // if (window.location.href.includes('auth/register')) {
        //     showLeftNotification(`Wlecome please fill the form to register`);
            
        // }
        if (window.location.href.includes('auth/reset')) {
            showLeftNotification("You have 10 inutes to reset password");
        }
    });


