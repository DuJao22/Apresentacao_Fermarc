/* Fermarc E-commerce - Main JavaScript
 * Desenvolvido por João Lion
 */

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// AJAX Add to Cart (optional enhancement)
function addToCartAjax(productId, quantity = 1) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    
    // Get CSRF token from meta tag or form
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    formData.append('csrf_token', csrfToken);
    
    fetch(`/cart/add/${productId}`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart count badge
            const cartBadge = document.querySelector('.cart-badge');
            if (cartBadge) {
                cartBadge.textContent = data.cart_count;
            }
            
            // Show success message
            showToast('success', data.message);
        } else {
            showToast('error', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('error', 'Erro ao adicionar produto ao carrinho');
    });
}

// Simple toast notification
function showToast(type, message) {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toastEl);
    
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
    
    toastEl.addEventListener('hidden.bs.toast', function() {
        toastEl.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

console.log('Fermarc E-commerce - Desenvolvido por João Lion');
