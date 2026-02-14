from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass

@dataclass
class GrainSigilMetadata:
    version: str = "1.2"
    issuer: str = "Survivor-Led Autonomy Network (Simulated)"
    issued_at: str = None
    identity_proof_hash: str = ""
    ethical_profile: List[str] = None
    capabilities: List[str] = None
    user_attributes: Dict[str, Any] = None
    proofs: Dict[str, str] = None
    linked_wallet_address: str = ""
    sigil_fingerprint: Optional[str] = None
    verifiable_credentials: List[Dict] = None

    def __post_init__(self):
        if self.issued_at is None:
            self.issued_at = datetime.now(timezone.utc).isoformat()
        if self.ethical_profile is None:
            self.ethical_profile = []
        if self.capabilities is None:
            self.capabilities = []
        if self.user_attributes is None:
            self.user_attributes = {}
        if self.proofs is None:
            self.proofs = {}
        if self.verifiable_credentials is None:
            self.verifiable_credentials = []

    def to_dict(self):
        return {
            'version': self.version,
            'issuer': self.issuer,
            'issued_at': self.issued_at,
            'identity_proof_hash': self.identity_proof_hash,
            'ethical_profile': self.ethical_profile,
            'capabilities': self.capabilities,
            'user_attributes': self.user_attributes,
            'proofs': self.proofs,
            'linked_wallet_address': self.linked_wallet_address,
            'sigil_fingerprint': self.sigil_fingerprint,
            'verifiable_credentials': self.verifiable_credentials
        }

@dataclass
class AccessPolicy:
    required_ethics: List[str] = None
    required_capabilities: List[str] = None
    attribute_conditions: Dict[str, Any] = None
    requires_proof_type: Optional[str] = None
    required_credentials: List[Dict[str, str]] = None

    def __post_init__(self):
        if self.required_ethics is None:
            self.required_ethics = []
        if self.required_capabilities is None:
            self.required_capabilities = []
        if self.attribute_conditions is None:
            self.attribute_conditions = {}
        if self.required_credentials is None:
            self.required_credentials = []

    def to_dict(self):
        return {
            'required_ethics': self.required_ethics,
            'required_capabilities': self.required_capabilities,
            'attribute_conditions': self.attribute_conditions,
            'requires_proof_type': self.requires_proof_type,
            'required_credentials': self.required_credentials
        }

@dataclass
class OnChainAction:
    function: str
    params: List[Any]

    def to_dict(self):
        return {
            'function': self.function,
            'params': self.params
        }

@dataclass
class DigitalLockConfig:
    type: str
    controls: str
    access_policy: AccessPolicy
    access_message: str
    on_chain_actions: List[OnChainAction] = None

    def __post_init__(self):
        if self.on_chain_actions is None:
            self.on_chain_actions = []

    def to_dict(self):
        return {
            'type': self.type,
            'controls': self.controls,
            'access_policy': self.access_policy.to_dict(),
            'access_message': self.access_message,
            'on_chain_actions': [action.to_dict() for action in self.on_chain_actions]
        }

@dataclass
class NftAsset:
    type: str
    id: str
    token_uri: Optional[str] = None
    mint_number: Optional[int] = None
    impact_tag: Optional[str] = None

    def to_dict(self):
        return {
            'type': self.type,
            'id': self.id,
            'token_uri': self.token_uri,
            'mint_number': self.mint_number,
            'impact_tag': self.impact_tag
        }

@dataclass
class WalletView:
    address: str
    CareTokens: float
    NFTs: List[NftAsset]

    def to_dict(self):
        return {
            'address': self.address,
            'CareTokens': self.CareTokens,
            'NFTs': [nft.to_dict() for nft in self.NFTs]
        }
