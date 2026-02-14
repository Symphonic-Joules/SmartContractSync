import hashlib
import json
import os
import logging
from typing import List, Dict, Optional
from web3 import Web3
# Import web3 middleware with compatibility for different versions
from dotenv import load_dotenv
from secrets_util import load_secret

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class BlockchainService:
    def __init__(self):
        # Load secrets with automatic decryption using your pattern
        try:
            # Decode your key safely from environment (encrypted secrets)
            self.SEPOLIA_RPC_URL = load_secret("SEPOLIA_RPC_URL", key="Grain")
        except ValueError:
            # Fallback to plain environment variable
            self.SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL", "http://localhost:8545")
        
        try:
            # Decode your key safely from environment (encrypted private key)
            self.SERVICE_PRIVATE_KEY = load_secret("SERVICE_PRIVATE_KEY", key="Grain")
        except ValueError:
            # Fallback to plain environment variable
            self.SERVICE_PRIVATE_KEY = os.getenv("SERVICE_PRIVATE_KEY")
        
        # Plain text contract addresses and ABIs
        self.BASIC_TRANSPARENCY_CONTRACT_ADDRESS = os.getenv("BASIC_TRANSPARENCY_CONTRACT_ADDRESS")
        self.BASIC_TRANSPARENCY_ABI = self._load_abi("BASIC_TRANSPARENCY_ABI_JSON")
        self.CARE_TOKEN_CONTRACT_ADDRESS = os.getenv("CARE_TOKEN_CONTRACT_ADDRESS")
        self.CARE_TOKEN_ABI = self._load_abi("CARE_TOKEN_ABI_JSON")
        self.TESTIMONY_NFT_CONTRACT_ADDRESS = os.getenv("TESTIMONY_NFT_CONTRACT_ADDRESS")
        self.TESTIMONY_NFT_ABI = self._load_abi("TESTIMONY_NFT_ABI_JSON")

        # Initialize Web3 instance
        self.w3 = Web3(Web3.HTTPProvider(self.SEPOLIA_RPC_URL))
        
        # Inject PoA middleware for Sepolia - simplified approach
        logger.info("Initializing Web3 without PoA middleware (compatible mode)")
        
        # Check connection
        if not self.w3.is_connected():
            logger.error("ERROR: Not connected to Sepolia Testnet! Check RPC URL and internet connection.")
        else:
            logger.info(f"Connected to Sepolia Testnet. Current block: {self.w3.eth.block_number}")

        # Initialize Service Account
        self.service_account = None
        if self.SERVICE_PRIVATE_KEY:
            self.service_account = self.w3.eth.account.from_key(self.SERVICE_PRIVATE_KEY)
            logger.info(f"Service account address: {self.service_account.address}")
        else:
            logger.warning("WARNING: SERVICE_PRIVATE_KEY not found. On-chain actions will fail.")

        # Initialize Contract Instances
        self.basic_transparency_contract = self._init_contract(
            self.BASIC_TRANSPARENCY_CONTRACT_ADDRESS, 
            self.BASIC_TRANSPARENCY_ABI,
            "BasicTransparency"
        )
        
        self.care_token_contract = self._init_contract(
            self.CARE_TOKEN_CONTRACT_ADDRESS,
            self.CARE_TOKEN_ABI,
            "CareToken"
        )
        
        self.testimony_nft_contract = self._init_contract(
            self.TESTIMONY_NFT_CONTRACT_ADDRESS,
            self.TESTIMONY_NFT_ABI,
            "TestimonyNFT"
        )

    def _load_abi(self, env_var_name: str) -> List[Dict]:
        """Load ABI from environment variable"""
        abi_json = os.getenv(env_var_name, "[]")
        try:
            return json.loads(abi_json)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {env_var_name}")
            return []

    def _load_abi_from_config(self, config_key: str) -> List[Dict]:
        """Load ABI from config dictionary"""
        abi_json = self.config.get(config_key, "[]")
        try:
            return json.loads(abi_json)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {config_key}")
            return []

    def _init_contract(self, address: Optional[str], abi: List[Dict], name: str):
        """Initialize a contract instance"""
        if address and abi:
            try:
                contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(address), 
                    abi=abi
                )
                logger.info(f"Loaded {name} contract at: {address}")
                return contract
            except Exception as e:
                logger.error(f"Failed to load {name} contract: {e}")
        return None

    def _send_transaction(self, contract_function, params: list, gas_limit: int) -> Dict:
        """Send a transaction to the blockchain"""
        if not self.service_account:
            return {
                "status": "error", 
                "reason": "Service account not configured (private key missing).", 
                "action": contract_function.__name__
            }

        try:
            nonce = self.w3.eth.get_transaction_count(self.service_account.address)
            gas_price = self.w3.eth.gas_price

            tx_dict = contract_function(*params).build_transaction({
                'from': self.service_account.address,
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx_dict, private_key=self.SERVICE_PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            logger.info(f"Tx sent: {tx_hash.hex()} for {contract_function.__name__}")
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Handle receipt access with compatibility for different web3.py versions
            tx_hash_hex = tx_hash.hex()
            status = getattr(receipt, 'status', receipt.get('status', 0))
            gas_used = getattr(receipt, 'gasUsed', receipt.get('gasUsed', 0))
            to_address = getattr(receipt, 'to', receipt.get('to', '0x0'))
            
            logger.info(f"Tx mined: {tx_hash_hex} status: {status}")

            if status == 1:
                return {
                    "transaction_hash": tx_hash_hex,
                    "status": "success",
                    "gas_used": gas_used,
                    "action": contract_function.__name__,
                    "contract_address": to_address.hex() if hasattr(to_address, 'hex') else str(to_address)
                }
            else:
                return {
                    "transaction_hash": tx_hash_hex,
                    "status": "failed",
                    "reason": "Transaction failed on-chain",
                    "gas_used": gas_used,
                    "action": contract_function.__name__
                }
        except Exception as e:
            logger.error(f"Failed to execute {contract_function.__name__}: {e}")
            return {"status": "error", "action": contract_function.__name__, "error": str(e)}

    def allocate_reparations(self, sigil_address: str, amount: float) -> Dict:
        """Allocate reparations by transferring CareTokens"""
        if not self.care_token_contract:
            return {"status": "error", "action": "allocate_reparations", "error": "CareToken contract not loaded."}
        
        # Convert to wei (assuming 18 decimals)
        amount_in_wei = self.w3.to_wei(amount, 'ether')

        return self._send_transaction(
            self.care_token_contract.functions.transfer,
            [Web3.to_checksum_address(sigil_address), amount_in_wei],
            100000
        )

    def mint_testimony_credit(self, sigil_address: str, impact_tag: str) -> Dict:
        """Mint a Testimony Credit NFT"""
        if not self.testimony_nft_contract:
            return {"status": "error", "action": "mint_testimony_credit", "error": "Testimony NFT contract not loaded."}
        
        testimony_metadata_uri = "ipfs://Qmb5xX5V5g7t3k9Y7z0d5xX5V5g7t3k9Y7z0d5xX5V5g7t3k9Y"
        
        return self._send_transaction(
            self.testimony_nft_contract.functions.mint,
            [Web3.to_checksum_address(sigil_address), testimony_metadata_uri],
            300000
        )

    def mint_creative_work(self, sigil_address: str, work_id: str) -> Dict:
        """Mint a Creative Work NFT"""
        if not self.testimony_nft_contract:
            return {"status": "error", "action": "mint_creative_work", "error": "Creative Work NFT contract not loaded."}
        
        creative_zine_token_uri = "ipfs://bafyreigbj4vldlhpsgw24ns3d24e2t62dxpftvt3e7n6a76fbdlmgz2agu/metadata.json"

        return self._send_transaction(
            self.testimony_nft_contract.functions.mint,
            [Web3.to_checksum_address(sigil_address), creative_zine_token_uri],
            300000
        )

    def update_reputation(self, user_address: str, score_change: int, action: str) -> Dict:
        """Update reputation on BasicTransparency contract"""
        if not self.basic_transparency_contract:
            return {"status": "error", "action": "update_reputation", "error": "BasicTransparency contract not loaded."}
        
        return self._send_transaction(
            self.basic_transparency_contract.functions.updateReputation,
            [Web3.to_checksum_address(user_address), score_change, action],
            200000
        )

    def submit_probe(self, submitter_address: str, target: str, question: str) -> Dict:
        """Submit a probe to BasicTransparency contract"""
        if not self.basic_transparency_contract:
            return {"status": "error", "action": "submit_probe", "error": "BasicTransparency contract not loaded."}
        
        return self._send_transaction(
            self.basic_transparency_contract.functions.submitProbe,
            [target, question],
            300000
        )

    def get_wallet_assets(self, wallet_address: str) -> Dict:
        """Get wallet assets including CareTokens and NFTs"""
        checksum_address = Web3.to_checksum_address(wallet_address)
        
        # Get CareToken balance
        care_tokens_balance = 0.0
        if self.care_token_contract:
            try:
                raw_balance = self.care_token_contract.functions.balanceOf(checksum_address).call()
                decimals = self.care_token_contract.functions.decimals().call()
                care_tokens_balance = raw_balance / (10**decimals)
            except Exception as e:
                logger.error(f"Could not fetch CareToken balance for {wallet_address}: {e}")
        
        # For NFTs, we'd need to implement additional logic or use external APIs like Alchemy
        owned_nfts = []
        
        return {
            "address": wallet_address,
            "CareTokens": care_tokens_balance,
            "NFTs": owned_nfts
        }

    def generate_sigil_fingerprint(self, sigil_data: Dict) -> str:
        """Generate a unique fingerprint for a sigil"""
        sigil_json = json.dumps(sigil_data, sort_keys=True)
        return hashlib.sha256(sigil_json.encode()).hexdigest()

    def check_access_policy(self, sigil_metadata: Dict, access_policy: Dict) -> tuple[bool, str]:
        """Check if a sigil meets the access policy requirements"""
        try:
            # Check required ethics
            required_ethics = access_policy.get('required_ethics', [])
            user_ethics = sigil_metadata.get('ethical_profile', [])
            
            if required_ethics and not all(ethic in user_ethics for ethic in required_ethics):
                missing_ethics = [ethic for ethic in required_ethics if ethic not in user_ethics]
                return False, f"Missing required ethics: {', '.join(missing_ethics)}"
            
            # Check required capabilities
            required_capabilities = access_policy.get('required_capabilities', [])
            user_capabilities = sigil_metadata.get('capabilities', [])
            
            if required_capabilities and not all(cap in user_capabilities for cap in required_capabilities):
                missing_caps = [cap for cap in required_capabilities if cap not in user_capabilities]
                return False, f"Missing required capabilities: {', '.join(missing_caps)}"
            
            # Check attribute conditions
            attribute_conditions = access_policy.get('attribute_conditions', {})
            user_attributes = sigil_metadata.get('user_attributes', {})
            
            for attr, expected_value in attribute_conditions.items():
                if attr not in user_attributes:
                    return False, f"Missing required attribute: {attr}"
                if user_attributes[attr] != expected_value:
                    return False, f"Attribute {attr} does not match required value"
            
            # Check proof type
            requires_proof_type = access_policy.get('requires_proof_type')
            if requires_proof_type:
                user_proofs = sigil_metadata.get('proofs', {})
                if requires_proof_type not in user_proofs:
                    return False, f"Missing required proof type: {requires_proof_type}"
            
            return True, "Access granted"
            
        except Exception as e:
            logger.error(f"Error checking access policy: {e}")
            return False, f"Error validating access: {str(e)}"

# Global blockchain service instance
blockchain_service = BlockchainService()
