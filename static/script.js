document.addEventListener('DOMContentLoaded', function() {
    // Set max date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').max = today;
    document.getElementById('date').value = today;

    // Form submission handler
    const digestForm = document.getElementById('digestForm');
    if (digestForm) {
        digestForm.addEventListener('submit', function(e) {
            const generateBtn = document.getElementById('generateBtn');
            const loadingSpinner = document.getElementById('loadingSpinner');
            
            // Show loading state
            generateBtn.disabled = true;
            loadingSpinner.classList.remove('hidden');
            generateBtn.innerHTML = 'Generating... ';
            generateBtn.appendChild(loadingSpinner);
        });
    }

    // Service Worker Registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then(registration => {
                    console.log('ServiceWorker registration successful');
                })
                .catch(err => {
                    console.log('ServiceWorker registration failed: ', err);
                });
        });
    }

    // Offline detection
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);

    function updateOnlineStatus() {
        const status = navigator.onLine ? 'online' : 'offline';
        if (status === 'offline') {
            showOfflineAlert();
        }
    }

    function showOfflineAlert() {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'fixed bottom-4 right-4 bg-red-600 text-white px-4 py-2 rounded shadow-lg';
        alertDiv.textContent = 'You are currently offline. Some features may not work.';
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Print functionality
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            window.print();
        }
    });

    // Initialize tooltips
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', showTooltip);
        el.addEventListener('mouseleave', hideTooltip);
    });

    function showTooltip(e) {
        const tooltipText = e.target.getAttribute('data-tooltip');
        const tooltip = document.createElement('div');
        tooltip.className = 'absolute z-10 bg-gray-900 text-white text-xs rounded py-1 px-2';
        tooltip.textContent = tooltipText;
        tooltip.id = 'current-tooltip';
        
        const rect = e.target.getBoundingClientRect();
        tooltip.style.top = `${rect.top - 30}px`;
        tooltip.style.left = `${rect.left + rect.width / 2}px`;
        tooltip.style.transform = 'translateX(-50%)';
        
        document.body.appendChild(tooltip);
    }

    function hideTooltip() {
        const tooltip = document.getElementById('current-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }
});