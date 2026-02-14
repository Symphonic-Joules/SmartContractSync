"""
Demo mode for Grain Sigil Autonomy Network
Provides mock blockchain functionality when real connections aren't available
"""
import hashlib
import json
import random
import time
from typing import Dict, List, Any

class DemoBlockchainService:
    """Mock blockchain service for demonstration purposes"""
    
    def __init__(self):
        self.connected = True
        self.demo_mode = True
        self.current_block = 12345678
        
    def generate_sigil_fingerprint(self, sigil_data: Dict) -> str:
        """Generate a unique fingerprint for a sigil"""
        # Create a hash from the sigil data
        data_string = json.dumps(sigil_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()[:16]
    
    def check_access_policy(self, sigil_metadata: Dict, access_policy: Dict) -> tuple[bool, str]:
        """Check if a sigil meets the access policy requirements"""
        required_ethics = access_policy.get('required_ethics', [])
        required_capabilities = access_policy.get('required_capabilities', [])
        attribute_conditions = access_policy.get('attribute_conditions', {})
        
        sigil_ethics = sigil_metadata.get('ethical_profile', [])
        sigil_capabilities = sigil_metadata.get('capabilities', [])
        sigil_attributes = sigil_metadata.get('user_attributes', {})
        
        # Check ethics requirements
        missing_ethics = [ethic for ethic in required_ethics if ethic not in sigil_ethics]
        if missing_ethics:
            return False, f"Missing required ethics: {', '.join(missing_ethics)}"
        
        # Check capabilities requirements
        missing_capabilities = [cap for cap in required_capabilities if cap not in sigil_capabilities]
        if missing_capabilities:
            return False, f"Missing required capabilities: {', '.join(missing_capabilities)}"
        
        # Check attribute conditions
        for attr_name, required_value in attribute_conditions.items():
            sigil_value = sigil_attributes.get(attr_name)
            if sigil_value != required_value:
                return False, f"Attribute '{attr_name}' does not match requirement"
        
        return True, "Access granted - all requirements met"
    
    def allocate_reparations(self, sigil_address: str, amount: float) -> Dict:
        """Mock reparations allocation"""
        return {
            "status": "success",
            "transaction_hash": f"0x{hashlib.sha256(f'reparations_{sigil_address}_{time.time()}'.encode()).hexdigest()}",
            "amount": amount,
            "recipient": sigil_address,
            "demo_mode": True
        }
    
    def mint_testimony_credit(self, sigil_address: str, impact_tag: str) -> Dict:
        """Mock testimony credit minting"""
        return {
            "status": "success",
            "transaction_hash": f"0x{hashlib.sha256(f'testimony_{sigil_address}_{impact_tag}_{time.time()}'.encode()).hexdigest()}",
            "token_id": random.randint(1000, 9999),
            "impact_tag": impact_tag,
            "recipient": sigil_address,
            "demo_mode": True
        }
    
    def mint_creative_work(self, sigil_address: str, work_id: str) -> Dict:
        """Mock creative work minting"""
        return {
            "status": "success",
            "transaction_hash": f"0x{hashlib.sha256(f'creative_{sigil_address}_{work_id}_{time.time()}'.encode()).hexdigest()}",
            "token_id": random.randint(1000, 9999),
            "work_id": work_id,
            "recipient": sigil_address,
            "demo_mode": True
        }
    
    def update_reputation(self, user_address: str, score_change: int, action: str) -> Dict:
        """Mock reputation update"""
        return {
            "status": "success",
            "transaction_hash": f"0x{hashlib.sha256(f'reputation_{user_address}_{action}_{time.time()}'.encode()).hexdigest()}",
            "score_change": score_change,
            "action": action,
            "user": user_address,
            "demo_mode": True
        }
    
    def submit_probe(self, submitter_address: str, target: str, question: str) -> Dict:
        """Mock probe submission"""
        return {
            "status": "success",
            "transaction_hash": f"0x{hashlib.sha256(f'probe_{submitter_address}_{target}_{time.time()}'.encode()).hexdigest()}",
            "probe_id": random.randint(100, 999),
            "target": target,
            "question": question,
            "submitter": submitter_address,
            "demo_mode": True
        }
    
    def get_wallet_assets(self, wallet_address: str) -> Dict:
        """Mock wallet assets"""
        return {
            "address": wallet_address,
            "CareTokens": round(random.uniform(10, 1000), 2),
            "NFTs": [
                {
                    "type": "Testimony Credit",
                    "id": f"TC{random.randint(100, 999)}",
                    "impact_tag": "survivor_support",
                    "mint_number": random.randint(1, 50)
                },
                {
                    "type": "Creative Work",
                    "id": f"CW{random.randint(100, 999)}",
                    "token_uri": f"ipfs://demo{random.randint(1000, 9999)}"
                }
            ],
            "demo_mode": True
        }

# Create demo service instance
demo_service = DemoBlockchainService()