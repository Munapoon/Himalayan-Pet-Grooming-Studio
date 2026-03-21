/**
 * Product Detail quantity controls and purchase actions.
 */
function incrementQty(max) {
    const qtyInput = document.getElementById('quantity');
    if (qtyInput) {
        const currentVal = parseInt(qtyInput.value) || 1;
        const maxValue = parseInt(max) || Infinity;
        if (currentVal < maxValue) {
            qtyInput.value = currentVal + 1;
        } else {
            alert('Cannot exceed available stock limit (' + maxValue + ' items)');
        }
    }
}

function decrementQty() {
    const qtyInput = document.getElementById('quantity');
    if (qtyInput) {
        const currentVal = parseInt(qtyInput.value) || 1;
        if (currentVal > 1) {
            qtyInput.value = currentVal - 1;
        }
    }
}

function buyNow() {
    const redirectTo = document.getElementById('redirectTo');
    const form = document.getElementById('addToCartForm');
    
    // Manual validation for size requirement since form.submit() bypasses onsubmit
    const sizeBlock = document.getElementById('sizeSelectionBlock');
    const sizeInput = document.getElementById('selectedSizeInput');
    if (sizeBlock && (!sizeInput || !sizeInput.value)) {
        alert('Please select a size first!');
        return;
    }

    if (redirectTo && form) {
        redirectTo.value = 'cart';
        form.submit();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Quantity increment
    const incrementBtns = document.querySelectorAll('.increment-btn');
    incrementBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            incrementQty(this.dataset.max);
        });
    });

    // Quantity decrement
    const decrementBtns = document.querySelectorAll('.decrement-btn');
    decrementBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            decrementQty();
        });
    });

    // Buy Now
    const buyNowBtn = document.querySelector('.btn-buy-now');
    if (buyNowBtn) {
        buyNowBtn.addEventListener('click', function () {
            buyNow();
        });
    }
});
