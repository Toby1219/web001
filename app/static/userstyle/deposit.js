document.addEventListener('DOMContentLoaded', function () {
    const investmentCards = document.querySelectorAll('.investment-card');
    const proceedButton = document.getElementById('proceedButton');
    const paymentConfirmationModal = new bootstrap.Modal(document.getElementById('paymentConfirmationModal'));
    const confirmPaymentBtn = document.getElementById('confirmPaymentBtn');
    const paymentConfirmedModal = new bootstrap.Modal(document.getElementById('paymentConfirmedModal'));
    const depositAmountInput = document.getElementById('depositAmount');
    const amountValidationFeedback = document.getElementById('amountValidationFeedback');
    const w_address = document.getElementById("modalWalletAddress").textContent;
    const w_type = document.getElementById("modalWalletType").textContent;

    let selectedPlanData = null;

    function showAmountFeedback(message, isValid) {
        amountValidationFeedback.textContent = message;
        amountValidationFeedback.classList.remove('d-none');
        amountValidationFeedback.classList.remove('text-success', 'text-danger');
        depositAmountInput.classList.remove('is-valid', 'is-invalid');

        if (isValid) {
            amountValidationFeedback.classList.add('text-success');
            depositAmountInput.classList.add('is-valid');
        } else {
            amountValidationFeedback.classList.add('text-danger');
            depositAmountInput.classList.add('is-invalid');
        }
    }

    function hideAmountFeedback() {
        amountValidationFeedback.classList.add('d-none');
        depositAmountInput.classList.remove('is-valid', 'is-invalid');
    }

    function updateProceedButtonState() {
        const amountValue = parseFloat(depositAmountInput.value);
        const isAmountEntered = !isNaN(amountValue) && amountValue > 0;
        let isAmountValid = false;

        hideAmountFeedback();

        if (selectedPlanData && isAmountEntered) {
            const min = parseFloat(selectedPlanData.minAmount);
            const max = parseFloat(selectedPlanData.maxAmount);

            if (amountValue >= min && amountValue <= max) {
                isAmountValid = true;
                showAmountFeedback(`Amount is within the plan range.`, true);
            } else {
                showAmountFeedback(`Amount must be between USD ${min.toFixed(2)} and USD ${max.toFixed(2)} for ${selectedPlanData.name}.`, false);
            }
        } else if (isAmountEntered) {
            showAmountFeedback("Please select an investment plan first.", false);
        } else if (!isAmountEntered && selectedPlanData) {
            showAmountFeedback("Please enter a valid deposit amount.", false);
        }

        proceedButton.disabled = !(selectedPlanData && isAmountEntered && isAmountValid);
    }

    investmentCards.forEach(card => {
        card.addEventListener('click', function () {
            investmentCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');

            selectedPlanData = {
                id: this.dataset.planId,
                name: this.dataset.planName,
                palnPercentage: this.dataset.planPercent,
                planHours: this.dataset.planHours,
                minAmount: this.dataset.minAmount,
                maxAmount: this.dataset.maxAmount,
                percentage: this.querySelector('.plan-percentage').textContent.trim(),
                priceRange: this.querySelector('.plan-price-range').textContent.trim(),
                refBy: this.dataset.refby,
                refcode: this.dataset.refcode
            };

            updateProceedButtonState();
        });
    });

    depositAmountInput.addEventListener('input', updateProceedButtonState);
    depositAmountInput.addEventListener('blur', updateProceedButtonState);

    proceedButton.addEventListener('click', function () {
        updateProceedButtonState();
        if (selectedPlanData && !proceedButton.disabled) {
            document.getElementById('modalSelectedPlanName').textContent = selectedPlanData.name;
            document.getElementById('modalDepositAmount').textContent = `USD ${parseFloat(depositAmountInput.value).toFixed(2)}`;

            paymentConfirmationModal.show();
        }
    });

    confirmPaymentBtn.addEventListener('click', function () {
        paymentConfirmationModal.hide();
        paymentConfirmedModal.show();

        function post_request() {
            let payload = {
                'tt': 'deposit',
                'plan': selectedPlanData.name,
                'planamt': parseFloat(depositAmountInput.value).toFixed(2),
                'wa': w_address,
                'wt': w_type,
                'pp': selectedPlanData.palnPercentage,
                'ph': selectedPlanData.planHours,
                'refby': selectedPlanData.refBy,
                'refcode': selectedPlanData.refcode
            }
            paymentConfirmedModal.hide();

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

        setTimeout(() => {
            paymentConfirmedModal.hide();
            post_request()
            location.reload();
            
        }, 2000);
    });

    updateProceedButtonState();
    hideAmountFeedback();
});