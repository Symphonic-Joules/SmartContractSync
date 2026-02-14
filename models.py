from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field
import json


@dataclass
class GrainSigilMetadata:
    version: str = "1.2"
    issuer: str = "Survivor-Led Autonomy Network (Simulated)"
    issued_at: Optional[str] = None
    identity_proof_hash: str = ""
    ethical_profile: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    user_attributes: Dict[str, Any] = field(default_factory=dict)
    proofs: Dict[str, str] = field(default_factory=dict)
    linked_wallet_address: str = ""
    sigil_fingerprint: Optional[str] = None
    verifiable_credentials: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        if self.issued_at is None:
            self.issued_at = datetime.now(timezone.utc).isoformat()

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
    required_ethics: List[str] = field(default_factory=list)
    required_capabilities: List[str] = field(default_factory=list)
    attribute_conditions: Dict[str, Any] = field(default_factory=dict)
    requires_proof_type: Optional[str] = None
    required_credentials: List[Dict[str, str]] = field(default_factory=list)

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
    on_chain_actions: List[OnChainAction] = field(default_factory=list)

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
