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
    if (redirectTo && form) {
        redirectTo.value = 'cart';
        form.submit();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Quantity increment
    const incrementBtns = document.querySelectorAll('.increment-btn');
    incrementBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            incrementQty(this.dataset.max);
        });
    });

    // Quantity decrement
    const decrementBtns = document.querySelectorAll('.decrement-btn');
    decrementBtns.forEach(btn => {
        btn.addEventListener('click', function () {
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
