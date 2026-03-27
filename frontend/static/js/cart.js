/**
 * Shopping Cart management functionality.
 * Handles quantity adjustments, item selection, and checkout processing.
 */

function incrementCartQty(itemId, maxQty) {
    const qtyInput = document.getElementById('qty-' + itemId);
    const form = document.getElementById('update-form-' + itemId);
    const btn = document.querySelector(`.cart-increment[data-item-id="${itemId}"]`);
    
    if (qtyInput && form) {
        let currentQty = parseInt(qtyInput.value) || 1;
        const max = parseInt(maxQty);
        
        if (currentQty < max) {
            qtyInput.value = currentQty + 1;
            form.submit();
        } else {
            if (btn) btn.disabled = false;
            alert('Cannot exceed available stock limit (' + max + ' items)');
        }
    }
}

function decrementCartQty(itemId) {
    const qtyInput = document.getElementById('qty-' + itemId);
    const form = document.getElementById('update-form-' + itemId);
    if (qtyInput && form) {
        const currentQty = parseInt(qtyInput.value) || 0;
        if (currentQty > 1) {
            qtyInput.value = currentQty - 1;
            form.submit();
        }
    }
}

function toggleAllItems() {
    const selectAll = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.cart-item-checkbox');
    if (selectAll) {
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAll.checked;
        });
        updateOrderSummary();
    }
}

function updateOrderSummary() {
    const checkboxes = document.querySelectorAll('.cart-item-checkbox:checked');
    const allCheckboxes = document.querySelectorAll('.cart-item-checkbox');
    const selectAll = document.getElementById('select-all');
    const checkoutBtn = document.getElementById('checkout-btn');

    let total = 0;
    let count = 0;

    checkboxes.forEach(checkbox => {
        total += parseFloat(checkbox.dataset.price) || 0;
        count++;
    });

    const countEl = document.getElementById('selected-count');
    const totalEl = document.getElementById('selected-total');
    const finalTotalEl = document.getElementById('final-total');

    if (countEl) countEl.textContent = count;
    if (totalEl) totalEl.textContent = total.toFixed(2);
    if (finalTotalEl) finalTotalEl.textContent = total.toFixed(2);

    if (selectAll) {
        selectAll.checked = (allCheckboxes.length > 0 && checkboxes.length === allCheckboxes.length);
    }

    if (checkoutBtn) {
        checkoutBtn.disabled = (count === 0);
    }
}

function proceedToCheckout(checkoutUrl) {
    const checkboxes = document.querySelectorAll('.cart-item-checkbox:checked');

    if (checkboxes.length === 0) {
        alert('Please select at least one item to checkout');
        return;
    }

    const selectedIds = Array.from(checkboxes).map(cb => cb.dataset.itemId);
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = checkoutUrl;

    const csrfTokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfTokenEl) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfTokenEl.value;
        form.appendChild(csrfInput);
    }

    selectedIds.forEach(id => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_items';
        input.value = id;
        form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
}

document.addEventListener('DOMContentLoaded', function () {
    updateOrderSummary();

    // Select all checkbox
    const selectAll = document.getElementById('select-all');
    if (selectAll) {
        selectAll.addEventListener('change', toggleAllItems);
    }

    // Individual item checkboxes
    const checkboxes = document.querySelectorAll('.cart-item-checkbox');
    checkboxes.forEach(cb => {
        cb.addEventListener('change', updateOrderSummary);
    });

    // Quantity increment buttons
    const incrementBtns = document.querySelectorAll('.cart-increment');
    incrementBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            if (this.disabled) return;
            this.disabled = true;
            incrementCartQty(this.dataset.itemId, this.dataset.stock);
        });
    });

    // Quantity decrement buttons
    const decrementBtns = document.querySelectorAll('.cart-decrement');
    decrementBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            if (this.disabled) return;
            this.disabled = true;
            decrementCartQty(this.dataset.itemId);
        });
    });

    // Checkout button
    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function () {
            const checkoutUrl = this.dataset.url;
            if (checkoutUrl) {
                proceedToCheckout(checkoutUrl);
            }
        });
    }
});
