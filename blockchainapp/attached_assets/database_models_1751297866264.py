from app import db
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from datetime import datetime, timezone

class Sigil(db.Model):
    """Database model for storing Grain Sigil metadata"""
    __tablename__ = 'sigils'
    
    id = Column(Integer, primary_key=True)
    sigil_fingerprint = Column(String(64), unique=True, nullable=False, index=True)
    version = Column(String(10), nullable=False, default="1.2")
    issuer = Column(String(255), nullable=False, default="Survivor-Led Autonomy Network")
    issued_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    identity_proof_hash = Column(String(64), nullable=False)
    ethical_profile = Column(JSON, nullable=False, default=list)
    capabilities = Column(JSON, nullable=False, default=list)
    user_attributes = Column(JSON, nullable=False, default=dict)
    proofs = Column(JSON, nullable=False, default=dict)
    linked_wallet_address = Column(String(42), nullable=False)
    verifiable_credentials = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        """Convert to dictionary format matching original dataclass"""
        return {
            'version': self.version,
            'issuer': self.issuer,
            'issued_at': self.issued_at.isoformat(),
            'identity_proof_hash': self.identity_proof_hash,
            'ethical_profile': self.ethical_profile or [],
            'capabilities': self.capabilities or [],
            'user_attributes': self.user_attributes or {},
            'proofs': self.proofs or {},
            'linked_wallet_address': self.linked_wallet_address,
            'sigil_fingerprint': self.sigil_fingerprint,
            'verifiable_credentials': self.verifiable_credentials or []
        }
    
    @classmethod
    def from_metadata(cls, metadata_dict, sigil_fingerprint):
        """Create Sigil from metadata dictionary"""
        return cls(
            sigil_fingerprint=sigil_fingerprint,
            version=metadata_dict.get('version', '1.2'),
            issuer=metadata_dict.get('issuer', 'Survivor-Led Autonomy Network'),
            identity_proof_hash=metadata_dict.get('identity_proof_hash', ''),
            ethical_profile=metadata_dict.get('ethical_profile', []),
            capabilities=metadata_dict.get('capabilities', []),
            user_attributes=metadata_dict.get('user_attributes', {}),
            proofs=metadata_dict.get('proofs', {}),
            linked_wallet_address=metadata_dict.get('linked_wallet_address', ''),
            verifiable_credentials=metadata_dict.get('verifiable_credentials', [])
        )

class Lock(db.Model):
    """Database model for storing Digital Lock configurations"""
    __tablename__ = 'locks'
    
    id = Column(Integer, primary_key=True)
    lock_id = Column(String(64), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False)
    controls = Column(Text, nullable=False)
    access_message = Column(Text, nullable=False)
    access_policy = Column(JSON, nullable=False)
    on_chain_actions = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        """Convert to dictionary format matching original dataclass"""
        return {
            'type': self.type,
            'controls': self.controls,
            'access_policy': self.access_policy or {},
            'access_message': self.access_message,
            'on_chain_actions': self.on_chain_actions or []
        }
    
    @classmethod
    def from_config(cls, config_dict, lock_id):
        """Create Lock from configuration dictionary"""
        return cls(
            lock_id=lock_id,
            type=config_dict.get('type', 'access_control'),
            controls=config_dict.get('controls', ''),
            access_message=config_dict.get('access_message', ''),
            access_policy=config_dict.get('access_policy', {}),
            on_chain_actions=config_dict.get('on_chain_actions', [])
        )

class AccessLog(db.Model):
    """Database model for logging access attempts"""
    __tablename__ = 'access_logs'
    
    id = Column(Integer, primary_key=True)
    sigil_fingerprint = Column(String(64), nullable=False, index=True)
    lock_id = Column(String(64), nullable=False, index=True)
    access_granted = Column(db.Boolean, nullable=False)
    message = Column(Text, nullable=False)
    transaction_receipts = Column(JSON, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            'id': self.id,
            'sigil_fingerprint': self.sigil_fingerprint,
            'lock_id': self.lock_id,
            'access_granted': self.access_granted,
            'message': self.message,
            'transaction_receipts': self.transaction_receipts or [],
            'timestamp': self.timestamp.isoformat()
        }