
document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const filterForm = document.getElementById('filterForm');

    if (!filterForm) return;

    
    const categoryId = urlParams.get('category');
    if (categoryId) {
        const select = document.getElementById('category');
        if (select) select.value = categoryId;
    }

    const sortBy = urlParams.get('sort');
    if (sortBy) {
        const select = document.getElementById('sort');
        if (select) select.value = sortBy;
    }

    
    const categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.addEventListener('change', () => filterForm.submit());
    }

    const sortSelect = document.getElementById('sort');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => filterForm.submit());
    }

    
    let searchTimeout;
    const searchInput = filterForm.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterForm.submit();
            }, 800);
        });
    }
});
