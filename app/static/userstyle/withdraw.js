document.addEventListener('DOMContentLoaded', function () {
    const paymentMethodSelect = document.getElementById('accountInput1');
    const accountInput = document.getElementById('accountInput2');
    const proceedToWithdrawBtn = document.getElementById('proceedToWithdrawBtn');
    const withdrawalAmountInput = document.getElementById('withdrawalAmount');
    const availableFundsAmount = document.querySelector('.available-funds-amount');
    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    const confirmWithdrawalAmount = document.getElementById('confirmWithdrawalAmount');
    const confirmPaymentMethod = document.getElementById('confirmPaymentMethod');
    const confirmAccountDetails = document.getElementById('confirmAccountDetails');
    const confirmWithdrawalBtn = document.getElementById('confirmWithdrawalBtn');

    function updateButtonState() {
        const isAmountEntered = parseFloat(withdrawalAmountInput.value) > 0;

        proceedToWithdrawBtn.disabled = !(isAmountEntered);
    }

    withdrawalAmountInput.addEventListener('input', updateButtonState);

    updateButtonState();

    document.getElementById('paymentMethodForm').addEventListener('submit', function (event) {
        event.preventDefault();

        confirmWithdrawalAmount.textContent = 'USD ' + parseFloat(withdrawalAmountInput.value).toFixed(2);
        confirmPaymentMethod.textContent = paymentMethodSelect.value.trim();
        confirmAccountDetails.textContent = accountInput.value.trim();

        confirmationModal.show();
    });

    function make_payment(stats) {
        let payload = {
            'tt': "withdraw",
            'st': stats,
            'amt': parseFloat(withdrawalAmountInput.value),
            "wa": accountInput.value,
            'wt': paymentMethodSelect.value
        }
        fetch(`${window.location.origin}/auth/user-account/payment`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {})
            .catch(error => {})
    }

    confirmWithdrawalBtn.addEventListener('click', function () {
        confirmationModal.hide();

        const currentFundsText = availableFundsAmount.textContent;
        const currentFunds = parseFloat(currentFundsText.replace('USD', '').replace(',', '').trim());
        if (currentFunds <= 0 || currentFunds < parseFloat(withdrawalAmountInput.value)) {
            errorModal.show();
            setTimeout(() => {
                make_payment("f");
                location.reload()
            }, 2000)
        } else {
            successModal.show();
            setTimeout(() => {
                make_payment("s");
                location.reload()
            }, 2000)
        }
    });
});


