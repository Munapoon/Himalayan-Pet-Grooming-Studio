
window.changeQty = function(amount) {
    const qtyInput = document.getElementById('quantity');
    const incBtn = document.querySelector('.increment-btn');
    if (!qtyInput || !incBtn) return;

    let currentVal = parseInt(qtyInput.value) || 1;
    const max = parseInt(incBtn.dataset.max) || 999;

    if (amount > 0) {
        if (currentVal < max) {
            qtyInput.value = currentVal + 1;
        } else {
            alert('Cannot exceed available stock limit (' + max + ' units)');
        }
    } else {
        if (currentVal > 1) {
            qtyInput.value = currentVal - 1;
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const buyNowBtn = document.querySelector('.btn-buy-now');
    if (buyNowBtn) {
        buyNowBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const redirectTo = document.getElementById('redirectTo');
            const form = document.getElementById('addToCartForm');
            
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
        });
    }
});
