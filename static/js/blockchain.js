// Blockchain-specific utility functions and Web3 integration
class BlockchainHelper {
    constructor() {
        this.web3 = null;
        this.isConnected = false;
        this.account = null;
    }

    // Initialize Web3 connection (for client-side interactions)
    async initWeb3() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                this.web3 = new Web3(window.ethereum);
                await window.ethereum.request({ method: 'eth_requestAccounts' });
                const accounts = await this.web3.eth.getAccounts();
                this.account = accounts[0];
                this.isConnected = true;
                return true;
            } catch (error) {
                console.error('Error connecting to MetaMask:', error);
                return false;
            }
        } else {
            console.warn('MetaMask not detected');
            return false;
        }
    }

    // Get current network
    async getNetwork() {
        if (!this.web3) return null;
        try {
            const chainId = await this.web3.eth.getChainId();
            return chainId;
        } catch (error) {
            console.error('Error getting network:', error);
            return null;
        }
    }

    // Switch to Sepolia network
    async switchToSepolia() {
        if (!window.ethereum) return false;
        
        try {
            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId: '0xaa36a7' }], // Sepolia chain ID
            });
            return true;
        } catch (error) {
            console.error('Error switching to Sepolia:', error);
            return false;
        }
    }

    // Format wei to ether
    formatEther(wei) {
        if (!this.web3) return '0';
        return this.web3.utils.fromWei(wei.toString(), 'ether');
    }

    // Format ether to wei
    parseEther(ether) {
        if (!this.web3) return '0';
        return this.web3.utils.toWei(ether.toString(), 'ether');
    }

    // Validate Ethereum address
    isValidAddress(address) {
        if (!this.web3) return /^0x[a-fA-F0-9]{40}$/.test(address);
        return this.web3.utils.isAddress(address);
    }

    // Get transaction receipt
    async getTransactionReceipt(txHash) {
        if (!this.web3) return null;
        try {
            return await this.web3.eth.getTransactionReceipt(txHash);
        } catch (error) {
            console.error('Error getting transaction receipt:', error);
            return null;
        }
    }

    // Monitor transaction status
    async waitForTransaction(txHash, callback) {
        if (!this.web3) return null;
        
        const checkTransaction = async () => {
            try {
                const receipt = await this.getTransactionReceipt(txHash);
                if (receipt) {
                    if (callback) callback(receipt);
                    return receipt;
                } else {
                    setTimeout(checkTransaction, 2000); // Check every 2 seconds
                }
            } catch (error) {
                console.error('Error monitoring transaction:', error);
                if (callback) callback(null, error);
            }
        };
        
        checkTransaction();
    }

    // Generate random wallet for testing
    generateRandomWallet() {
        if (!this.web3) return null;
        return this.web3.eth.accounts.create();
    }

    // Sign message with current account
    async signMessage(message) {
        if (!this.web3 || !this.account) return null;
        
        try {
            const signature = await this.web3.eth.personal.sign(message, this.account);
            return signature;
        } catch (error) {
            console.error('Error signing message:', error);
            return null;
        }
    }

    // Verify signed message
    verifySignature(message, signature, address) {
        if (!this.web3) return false;
        
        try {
            const recoveredAddress = this.web3.eth.accounts.recover(message, signature);
            return recoveredAddress.toLowerCase() === address.toLowerCase();
        } catch (error) {
            console.error('Error verifying signature:', error);
            return false;
        }
    }
}

// Create global blockchain helper instance
const blockchainHelper = new BlockchainHelper();

// Auto-initialize Web3 if MetaMask is available
if (typeof window !== 'undefined') {
    window.addEventListener('load', async () => {
        const connected = await blockchainHelper.initWeb3();
        if (connected) {
            console.log('Web3 initialized successfully');
            
            // Check if we're on Sepolia
            const chainId = await blockchainHelper.getNetwork();
            if (chainId !== 11155111) { // Sepolia chain ID
                console.warn('Not connected to Sepolia testnet');
            }
        }
    });

    // Listen for account changes
    if (window.ethereum) {
        window.ethereum.on('accountsChanged', (accounts) => {
            if (accounts.length > 0) {
                blockchainHelper.account = accounts[0];
                console.log('Account changed to:', accounts[0]);
            } else {
                blockchainHelper.account = null;
                blockchainHelper.isConnected = false;
            }
        });

        window.ethereum.on('chainChanged', (chainId) => {
            console.log('Network changed to:', chainId);
            window.location.reload(); // Reload page on network change
        });
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BlockchainHelper, blockchainHelper };
}
