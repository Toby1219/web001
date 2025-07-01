document.addEventListener('DOMContentLoaded', function() {
    const transactionsTableBody = document.querySelector('.transactions-table');
    const receiptModal = new bootstrap.Modal(document.getElementById('receiptModal'));
    const receiptIdSpan = document.getElementById('receiptId');
    const receiptTimeSpan = document.getElementById('receiptTime');
    const receiptDateSpan = document.getElementById('receiptDate');
    const receiptAmountSpan = document.getElementById('receiptAmount');
    const receiptWTSpan = document.getElementById('receiptWalletType');
    const receiptWASpan = document.getElementById('receiptWalletAddress');
    const receiptTOSpan = document.getElementById('receiptTo');
    const receiptStatusSpan = document.getElementById('receiptStatus');
    const receiptTTSpan = document.getElementById('receiptTransacType');
    const remark = document.getElementById("receiptTransacRemark");
    const downloadReceiptBtn = document.getElementById('downloadReceiptBtn');

    transactionsTableBody.addEventListener('click', function(event) {
        if (event.target) {
            const row = event.target.closest('tr');   
            if (row) {
                receiptIdSpan.textContent = row.dataset.id;
                receiptTimeSpan.textContent = row.dataset.time;
                receiptDateSpan.textContent = row.dataset.date;
                receiptAmountSpan.textContent = row.dataset.amount;
                receiptWTSpan.textContent = row.dataset.wt;
                receiptWASpan.textContent = row.dataset.wa;
                receiptTOSpan.textContent = row.dataset.to;
                receiptStatusSpan.textContent = row.querySelector('.status-badge').textContent;
                receiptTTSpan.textContent = row.dataset.tt;
                remark.textContent = row.dataset.r;
                receiptModal.show();
            }
        }
    });

    downloadReceiptBtn.addEventListener('click', function() {
        const dummyImageURL = "https://placehold.co/600x400/808080/FFFFFF?text=Receipt+Image";
        const a = document.createElement('a');
        a.href = dummyImageURL;
        a.download = `receipt_${receiptIdSpan.textContent.replace('#', '')}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        receiptModal.hide();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    const filterDateFromInput = document.getElementById('filterDateFrom');
    const filterDateToInput = document.getElementById('filterDateTo');
    const filterStatusSelect = document.getElementById('filterStatus');
    const filterTypeSelect = document.getElementById('filterType');
    const activeFiltersDisplay = document.getElementById('activeFiltersDisplay');

    function saveFilters() {
        localStorage.setItem('filterDateFrom', filterDateFromInput.value);
        localStorage.setItem('filterDateTo', filterDateToInput.value);
        localStorage.setItem('filterStatus', filterStatusSelect.value);
        localStorage.setItem('filterType', filterTypeSelect.value);
        displayActiveFilters();
    }

    function loadFilters() {
        const savedDateFrom = localStorage.getItem('filterDateFrom');
        const savedDateTo = localStorage.getItem('filterDateTo');
        const savedStatus = localStorage.getItem('filterStatus');
        const savedType = localStorage.getItem('filterType');

        if (savedDateFrom) {
            filterDateFromInput.value = savedDateFrom;
        } else {
            const today = new Date();
            const twoDaysAgo = new Date(today);
            twoDaysAgo.setDate(today.getDate() - 2);
            filterDateFromInput.value = formatDate(twoDaysAgo);
        }

        if (savedDateTo) {
            filterDateToInput.value = savedDateTo;
        } else {
            const today = new Date();
            filterDateToInput.value = formatDate(today);
        }

        if (savedStatus) {
            filterStatusSelect.value = savedStatus;
        }

        if (savedType) {
            filterTypeSelect.value = savedType;
        }

        displayActiveFilters();
    }

    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function displayActiveFilters() {
        activeFiltersDisplay.innerHTML = '';

        const currentStatus = filterStatusSelect.value;
        const currentType = filterTypeSelect.value;
        const currentFromDate = filterDateFromInput.value;
        const currentToDate = filterDateToInput.value;

        if (currentStatus !== 'all') {
            const statusTag = createFilterTag(`Status: ${filterStatusSelect.options[filterStatusSelect.selectedIndex].text}`, 'status');
            activeFiltersDisplay.appendChild(statusTag);
        }

        if (currentType !== 'all') {
            const typeTag = createFilterTag(`Type: ${filterTypeSelect.options[filterTypeSelect.selectedIndex].text}`, 'type');
            activeFiltersDisplay.appendChild(typeTag);
        }

        if (currentFromDate) {
            const fromDateTag = createFilterTag(`From: ${currentFromDate}`, 'dateFrom');
            activeFiltersDisplay.appendChild(fromDateTag);
        }

        if (currentToDate) {
            const toDateTag = createFilterTag(`To: ${currentToDate}`, 'dateTo');
            activeFiltersDisplay.appendChild(toDateTag);
        }

        if (currentStatus !== 'all' || currentType !== 'all' || currentFromDate || currentToDate) {
            const clearAllBtn = document.createElement('button');
            clearAllBtn.classList.add('btn', 'clear-all-filters-btn');
            clearAllBtn.textContent = 'Clear All Filters';
            clearAllBtn.addEventListener('click', clearAllFilters);
            activeFiltersDisplay.appendChild(clearAllBtn);
        }
    }

    function createFilterTag(text, filterKey) {
        const tag = document.createElement('span');
        tag.classList.add('filter-tag');
        tag.innerHTML = `${text} <button type="button" class="clear-filter-btn" data-filter-key="${filterKey}">&times;</button>`;
        return tag;
    }

    activeFiltersDisplay.addEventListener('click', function(event) {
        if (event.target.classList.contains('clear-filter-btn')) {
            const filterKey = event.target.dataset.filterKey;
            
            switch(filterKey) {
                case 'status':
                    filterStatusSelect.value = 'all';
                    break;
                case 'type':
                    filterTypeSelect.value = 'all';
                    break;
                case 'dateFrom':
                    filterDateFromInput.value = '';
                    break;
                case 'dateTo':
                    filterDateToInput.value = '';
                    break;
            }
            saveFilters();
            filterForm.submit();
        }
    });

    function clearAllFilters() {
        filterDateFromInput.value = '';
        filterDateToInput.value = '';
        filterStatusSelect.value = 'all';
        filterTypeSelect.value = 'all';
        saveFilters();
        filterForm.submit();
    }

    loadFilters();

    filterForm.addEventListener('submit', function(event) {
        saveFilters();
    });

    filterDateFromInput.addEventListener('change', saveFilters);
    filterDateToInput.addEventListener('change', saveFilters);
    filterStatusSelect.addEventListener('change', saveFilters);
    filterTypeSelect.addEventListener('change', saveFilters);
});