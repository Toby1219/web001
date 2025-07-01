document.addEventListener('DOMContentLoaded', function () {
    const email = document.getElementById('email');
    const phoneInputw = document.getElementById('phonew');
    const phoneInputt = document.getElementById('phonet');
    const saveButton = document.getElementById('saveButton');
    function updateSaveButtonState() {
        const isphoneFilledw = phoneInputw.value.trim() !== '';
        const isphoneFilledt = phoneInputt.value.trim() !== '';
        const isEmailFilled = email.value.trim() !== "";
        saveButton.disabled = !(isphoneFilledw && isphoneFilledt && isEmailFilled);
    }
    email.addEventListener('input', updateSaveButtonState);
    phoneInputw.addEventListener('input', updateSaveButtonState);
    phoneInputt.addEventListener('input', updateSaveButtonState);
    updateSaveButtonState();
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

document.addEventListener('DOMContentLoaded', function() {
    const updateWalletsBtn = document.getElementById('updateButton');
    const updateRefComBtn = document.getElementById('updateButtonrefC');
    const walletInputs = document.querySelectorAll("#walletAddress");
    const ref_comsInput = document.querySelectorAll("#ref_coms");
    let data_payload = {};

    updateWalletsBtn.addEventListener('click', function(){
        walletInputs.forEach(ele => {
            data_payload[ele.dataset.wallet] = ele.value;
        });
        fetch(`${window.location.origin}/admin/get-wallet`, {
            method:"POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data_payload)
        })
        .then(response => response.json())
        .then(data => {
            {}
        })
        .catch(error => {
            {}
        });
        setTimeout(() => {
            window.location.href = `${window.location.origin}/admin/admin-setting`;
        }, 1500);
    });
    updateRefComBtn.addEventListener('click', function(){
        ref_comsInput.forEach(ele => {
            data_payload[ele.dataset.val] = ele.value;
        });
        console.log(data_payload);
        fetch(`${window.location.origin}/admin/get-ref-com`, {
            method:"POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data_payload)
        })
        .then(response => response.json())
        .then(data => {
            {}
        })
        .catch(error => {
            {}
        });
        setTimeout(() => {
            window.location.href = `${window.location.origin}/admin/admin-setting`;
        }, 1500);
    });
});



