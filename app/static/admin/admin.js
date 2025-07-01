document.addEventListener('DOMContentLoaded', function () {
    const transactionsTableBody = document.querySelector('.transactions-table');
    const receiptModal = new bootstrap.Modal(document.getElementById('receiptModal'));
    const receiptIdSpan = document.getElementById('receiptId');
    const receiptTimeSpan = document.getElementById('receiptTime');
    const receiptDateSpan = document.getElementById('receiptDate');
    const receiptAmountSpan = document.getElementById('receiptAmount');
    const receiptPlanSpan = document.getElementById('receiptPlan');
    const receiptWTSpan = document.getElementById('receiptWalletType');
    const receiptWASpan = document.getElementById('receiptWalletAddress');
    const receiptTOSpan = document.getElementById('receiptTo');
    const receiptStatusSpan = document.getElementById('receiptStatus');
    const receiptTTSpan = document.getElementById('receiptTransacType');
    const remark = document.getElementById("receiptTransacRemark")
    const name = document.getElementById("receiptName")


    const confirmWithdrawalAmount = document.getElementById("confirmWithdrawalAmount")

    const AcceptBtn = document.getElementById("AcceptPayment");
    const DeclineBtn = document.getElementById("DeclinePayment");

    // Initialize new modals
    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    const confirmBtn = document.getElementById('confirmBtn');
    const newRemarkText = document.getElementById('newRemarktext');


    AcceptBtn.addEventListener('click', function () {
        receiptModal.hide();
        confirmWithdrawalAmount.textContent = receiptAmountSpan.value
        let n = document.getElementById('n0');
        n.textContent = `Accepting ${name.innerText}`;
        newRemarkText.value = `Payment of ${receiptAmountSpan.value} is successfull`;
        confirmationModal.show()
        errorModal.hide()
        confirmBtn.addEventListener('click', function () {
            // Request payment
            if (n.innerText.includes('Accepting')) {
                let n = document.getElementById('n1');

                let transact = receiptTTSpan.innerText[0].toLowerCase().trim();
                let id = receiptIdSpan.innerText;
            
                let payload0 = {
                    'id':id,
                    'amt':receiptAmountSpan.value,
                    'r':newRemarkText.value,
                    'tt':transact,
                    'ac':'success' 
                }
                fetch(`${window.location.origin}/admin/update`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload0)
                })
                .then(response => response.json())
                .then(data => {
                    {}
                })
                .catch(error => {
                    {}
                })


                let payload1 = { 
                    'name': name.textContent, 
                    "amt":receiptAmountSpan.value,
                    "plan":receiptPlanSpan.value
                }
                fetch(`${window.location.origin}/admin/UpdateRefBal`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload1)
                })
                    .then(response => response.json())
                    .then(data => {
                        {}
                    })
                    .catch(error => {
                        {}
                    })
                console.log(payload1)
                n.textContent = name.innerText;
                confirmationModal.hide()
                successModal.show()
                setTimeout(() => {
                    location.reload();
                }, 1000);
            }

        })

    })

    DeclineBtn.addEventListener('click', function () {
        receiptModal.hide();
        confirmWithdrawalAmount.textContent = receiptAmountSpan.value
        let n = document.getElementById('n0');
        n.textContent = `Declineing ${name.innerText}`;
        newRemarkText.value = `Payment of ${receiptAmountSpan.value} Failed please try again`;
        confirmationModal.show()
        confirmBtn.addEventListener('click', function () {
            confirmationModal.hide()
            if (n.innerText.includes('Declineing')) {

                let transact = receiptTTSpan.innerText[0].toLowerCase().trim();
                let id = receiptIdSpan.innerText;

                let payload0 = {
                    'id':id,
                    'amt':receiptAmountSpan.value,
                    'r':newRemarkText.value,
                    'tt':transact,
                    'ac':'failed' 
                }
                fetch(`${window.location.origin}/admin/update`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload0)
                })
                .then(response => response.json())
                .then(data => {
                    {}
                })
                .catch(error => {
                    {}
                })

                let n = document.getElementById('n2');
                n.textContent = name.innerText;
                errorModal.show();
            }
            setTimeout(() => {
                location.reload();
            }, 1000);

        })

    })


    transactionsTableBody.addEventListener('click', function (event) {
        if (event.target) {
            const row = event.target.closest('tr');
            let status_ = row.querySelector('.status-badge').textContent
            console.log("Make Api call")
            if (row) {
                receiptIdSpan.textContent = row.dataset.id;
                receiptTimeSpan.textContent = row.dataset.time;
                receiptDateSpan.textContent = row.dataset.date;
                receiptAmountSpan.value = row.dataset.amount;
                receiptPlanSpan.value = row.dataset.plan
                receiptWTSpan.textContent = row.dataset.wt
                receiptWASpan.textContent = row.dataset.wa
                receiptTOSpan.textContent = row.dataset.to
                receiptStatusSpan.textContent = row.querySelector('.status-badge').textContent;
                receiptTTSpan.textContent = row.dataset.tt
                remark.textContent = row.dataset.r
                name.textContent = row.dataset.name

                receiptModal.show();
            }


        }

    });

})




