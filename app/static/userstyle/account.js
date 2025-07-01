let previousURL = document.referrer;

document.addEventListener('DOMContentLoaded', function() {
    const successModal = new bootstrap.Modal(document.getElementById('registrationSuccessModal'));
    const textOne = document.getElementById("registrationSuccessModalLabel");
    const modalTextElement = document.querySelector('.modal-text');
    const registrationSuccessModalElement = document.getElementById('registrationSuccessModal');

    registrationSuccessModalElement.addEventListener('shown.bs.modal', function () {
        if (modalTextElement) {
            modalTextElement.classList.add('blink-animation');
        }
    });

    registrationSuccessModalElement.addEventListener('hidden.bs.modal', function () {
        if (modalTextElement) {
            modalTextElement.classList.remove('blink-animation');
        }
    });

    function showAndHideSuccessModal(text) {
        let previousURL = document.referrer;
        if (previousURL.includes("auth/login")) {
            textOne.textContent = text;
        }
        successModal.show();
        setTimeout(() => {
            successModal.hide();
        }, 3500);
    }

    if (previousURL.includes("auth/login")) {
        showAndHideSuccessModal("Login Successful!");
    } else if (previousURL.includes('auth/register')) {
        showAndHideSuccessModal('Registration Successful!');
    }
});
