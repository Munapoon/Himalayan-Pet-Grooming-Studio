
document.addEventListener('DOMContentLoaded', function () {
    
    const toasts = document.querySelectorAll('.admin-toast');
    toasts.forEach(function (toast, index) {
        setTimeout(function () {
            toast.classList.add('removing');
            setTimeout(function () {
                toast.remove();
                
                const container = document.getElementById('admin-toast-container');
                if (container && container.children.length === 0) {
                    container.remove();
                }
            }, 300);
        }, 4000 + index * 300); 
    });
});
