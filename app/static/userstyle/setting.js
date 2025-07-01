document.addEventListener('DOMContentLoaded', function () {
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phonen');
    const saveButton = document.getElementById('saveButton');

    function updateSaveButtonState() {
        const isEmailFilled = emailInput.value.trim() !== '';
        const isphoneFilled = phoneInput.value.trim() !== '';

        saveButton.disabled = !(isphoneFilled && isEmailFilled);
    }

    emailInput.addEventListener('input', updateSaveButtonState);
    phoneInput.addEventListener('input', updateSaveButtonState);

    updateSaveButtonState();

    const profilePicUpload = document.getElementById('profilePicUpload');
    const changeProfilePicBtn = document.getElementById('changeProfilePicBtn');
    const profileIcon = document.querySelector('.profile-icon-wrapper .profile-icon');

    changeProfilePicBtn.addEventListener('click', function () {
        profilePicUpload.click();
    });

    profilePicUpload.addEventListener('change', function (event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = "Profile Picture";
                img.classList.add('profile-icon-image');
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.borderRadius = '50%';
                img.style.objectFit = 'cover';

                const iconWrapper = profileIcon.parentElement;
                iconWrapper.innerHTML = '';
                iconWrapper.appendChild(img);
            };

            reader.readAsDataURL(file);
        }
    });
});

const togglePasswordButtons = document.querySelectorAll('.toggle-password');

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
    if (window.location.href.includes('user-account/setting')) {
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
});