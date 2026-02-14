function loadBlockchainStatus() {
    fetch('/api/blockchain-status')
        .then(response => response.json())
        .then(data => {
            const statusDiv = document.getElementById('blockchain-status');
            if (!statusDiv) return;

            if (data.connected) {
                statusDiv.innerHTML = `
                    <span class="badge bg-success me-3"><i class="fas fa-check-circle me-1"></i>Connected</span>
                    <span class="text-muted">Block: ${data.block_number || 'N/A'}</span>
                `;
            } else {
                statusDiv.innerHTML = `
                    <span class="badge bg-warning me-3"><i class="fas fa-exclamation-triangle me-1"></i>Demo Mode</span>
                    <span class="text-muted">Running with simulated blockchain data</span>
                `;
            }
        })
        .catch(error => {
            const statusDiv = document.getElementById('blockchain-status');
            if (statusDiv) {
                statusDiv.innerHTML = `
                    <span class="badge bg-warning me-3"><i class="fas fa-exclamation-triangle me-1"></i>Demo Mode</span>
                    <span class="text-muted">Running with simulated blockchain data</span>
                `;
            }
        });
}
