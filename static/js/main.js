// Auto-dismiss alerts after 3s
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(a => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(a);
            bsAlert.close();
        });
    }, 3000);
});

// Simple counter animation for cart badge
const cartBadge = document.querySelector('.badge.rounded-pill');
if (cartBadge) {
    cartBadge.style.transition = 'transform 0.3s';
    cartBadge.style.transform = 'scale(1.3)';
    setTimeout(() => cartBadge.style.transform = 'scale(1)', 300);
}