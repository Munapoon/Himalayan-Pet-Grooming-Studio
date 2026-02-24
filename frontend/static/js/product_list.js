/**
 * Product List filtering and auto-submit functionality.
 */
document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const filterForm = document.getElementById('filterForm');

    if (!filterForm) return;

    // Set initial values from URL for category and sort dropdowns
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

    // Auto-submit form when category or sort option changes
    const categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.addEventListener('change', () => filterForm.submit());
    }

    const sortSelect = document.getElementById('sort');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => filterForm.submit());
    }

    // Auto-submit search after typing with a debounce delay (800ms)
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
