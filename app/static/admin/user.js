document.addEventListener('DOMContentLoaded', function () {
    const userEditModal = new bootstrap.Modal(document.getElementById('userEditModal'));
    const confirmChangesModal = new bootstrap.Modal(document.getElementById('confirmChangesModal'));
    const usersTableBody = document.querySelector('.users-table');
    const editUserNameSpan = document.getElementById('editUserName');
    const editUserNameInput = document.getElementById('editUserNameInput');
    const editUserEmailInput = document.getElementById('editUserEmail');
    const editUserReferralByInput = document.getElementById('editUserReferralBY');
    const editUserBalanceInput = document.getElementById('editUserBalance');
    const editUserReferralCountInput = document.getElementById('editUserReferralCount');
    const editUserPlanSelect = document.getElementById('editUserPlan');
    const editUserReferralCode = document.getElementById('editUserReferralCode');
    const editUserPass = document.getElementById('editUserPasswrd');
    const editUserBalance = document.getElementById('editUserBalance');
    const editUserInvested = document.getElementById('editUserInvested');
    const editUserEarned = document.getElementById('editUserEarned');
    const editUserPending = document.getElementById('editUserPending');
    const editUserID = document.getElementById('editUserID');
    const editUserPhone = document.getElementById('editUserPhone');
    const editUserWalletAddress = document.getElementById('editUserWalletAddress');
    const editUserWalletType = document.getElementById('editUserWalletType');
    const editUserRefEarnings = document.getElementById('editUserRefEarnings');
    const finalizeEditBtn = document.getElementById('finalizeEditBtn');
    const NoBtn = document.getElementById('NoBtn');
    const editUserPlan = document.getElementById('editUserPlan');
    const SaveBtn = document.getElementById('SaveBtn');
    const totalTransac = document.getElementById('totalTransac');
    const tactionBtn = document.getElementById('tactionBtn');

    tactionBtn.addEventListener('click', function () {
        window.location.href = '/admin/admin-transactions';
    });

    async function request(url) {
        try {
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            let data = await response.json();
            return data;
        } catch (error) {
            console.error("Fetch failed:", error);
            return null;
        }
    }

    usersTableBody.addEventListener('click', async function (event) {
        const row = event.target.closest('tr');
        let respo = await request(`${window.location.origin}/admin/get_user?t=${row.dataset.name}`);
        if (row) {
            editUserNameSpan.textContent = row.dataset.name;
            editUserNameInput.value = row.dataset.name;
            editUserEmailInput.value = row.dataset.email;
            editUserReferralByInput.value = row.dataset.refby;
            editUserReferralCode.value = row.dataset.refcode;
            editUserBalanceInput.value = row.dataset.balance;
            editUserReferralCountInput.value = row.dataset.refcount;
            editUserRefEarnings.value = respo['ref_earning'];
            editUserPlanSelect.value = row.dataset.plan;
            editUserPass.value = await respo['password'];
            editUserPlan.value = await respo['plan'];
            totalTransac.textContent = `Total Transaction by ${row.dataset.name} is ${await respo['total_transac']}`;
            editUserPhone.value = row.dataset.phone;
            editUserWalletAddress.value = respo['wa'];
            editUserWalletType.value = respo['wt'];
            editUserBalance.value = await respo['balance'];
            editUserInvested.value = await respo['invsted'];
            editUserEarned.value = await respo['earned'];
            editUserPending.value = await respo['ammount'];
            editUserID.value = await respo['id'];
            userEditModal.show();
        }
    });

    SaveBtn.addEventListener('click', function () {
        userEditModal.hide();
        confirmChangesModal.show();
    });

    NoBtn.addEventListener('click', function () {
        confirmChangesModal.hide();
        userEditModal.show();
    });

    finalizeEditBtn.addEventListener('click', function () {
        confirmChangesModal.hide();
        const payload = {
            "id": editUserID.value,
            'username': editUserNameSpan.textContent,
            'passwrd': editUserPass.value,
            'balance': editUserBalance.value,
            'invested': editUserInvested.value,
            'earned': editUserEarned.value,
            'pending': editUserPending.value,
            'activeplan': editUserPlan.value,
        };
        fetch(`${window.location.origin}/admin/udate_user`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                {}
            })
            .catch(error => {
                {}
            });
    });
});