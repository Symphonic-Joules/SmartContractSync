"""
Secure secrets utility for the Grain Sigil Autonomy Network
Handles encrypted secret loading with fallback to environment variables
"""
import os
import base64
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


logger = logging.getLogger(__name__)


def derive_key(password: str, salt: bytes = b'grain_sigil_salt') -> bytes:
    """Derive encryption key from password using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_secret(secret: str, key_password: str) -> str:
    """Encrypt a secret using the provided key password"""
    key = derive_key(key_password)
    f = Fernet(key)
    encrypted = f.encrypt(secret.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def encode_for_env(secret: str, key: str = "Grain") -> str:
    """
    Convenient alias for encrypting secrets for environment storage
    
    Args:
        secret: The secret value to encrypt
        key: The encryption key (default: "Grain")
        
    Returns:
        Encrypted string ready for Replit Secrets
    """
    return encrypt_secret(secret, key)


def decrypt_secret(encrypted_secret: str, key_password: str) -> str:
    """Decrypt a secret using the provided key password"""
    try:
        key = derive_key(key_password)
        f = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_secret.encode())
        decrypted = f.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception as e:
        logger.error(f"Failed to decrypt secret: {e}")
        raise ValueError("Invalid encryption key or corrupted secret")


def load_secret(env_var_name: str, key: str = None) -> str:
    """
    Load a secret from environment variables with optional decryption
    
    Args:
        env_var_name: Name of the environment variable
        key: Optional decryption key. If provided, assumes value is encrypted
        
    Returns:
        Decrypted secret value or raw environment variable
        
    Raises:
        ValueError: If secret not found or decryption fails
    """
    # First try to get from environment
    secret_value = os.getenv(env_var_name)
    
    if not secret_value:
        logger.error(f"Secret '{env_var_name}' not found in environment variables")
        raise ValueError(f"Required secret '{env_var_name}' not configured")
    
    # If no decryption key provided, return raw value
    if not key:
        return secret_value
    
    # Try to decrypt the value
    try:
        decrypted = decrypt_secret(secret_value, key)
        logger.info(f"Successfully decrypted secret '{env_var_name}'")
        return decrypted
    except Exception as e:
        logger.warning(f"Failed to decrypt '{env_var_name}', returning raw value: {e}")
        # Fallback to raw value if decryption fails
        return secret_value


def get_blockchain_config() -> dict:
    """
    Load all blockchain configuration secrets for the Grain Sigil Network
    
    Returns:
        Dictionary with all required blockchain configuration
    """
    config = {}
    
    # Required secrets
    required_secrets = [
        'SEPOLIA_RPC_URL',
        'SERVICE_PRIVATE_KEY',
        'BASIC_TRANSPARENCY_CONTRACT_ADDRESS',
        'CARE_TOKEN_CONTRACT_ADDRESS',
        'TESTIMONY_NFT_CONTRACT_ADDRESS',
        'BASIC_TRANSPARENCY_ABI_JSON',
        'CARE_TOKEN_ABI_JSON',
        'TESTIMONY_NFT_ABI_JSON'
    ]
    
    # Optional secrets with encryption support
    encrypted_secrets = [
        'SERVICE_PRIVATE_KEY',
        'SEPOLIA_RPC_URL'
    ]
    
    for secret_name in required_secrets:
        try:
            # Check if this secret might be encrypted
            if secret_name in encrypted_secrets:
                # Try with decryption key first
                try:
                    config[secret_name] = load_secret(secret_name, key="Grain")
                    logger.info(f"Loaded encrypted secret: {secret_name}")
                except:
                    # Fallback to unencrypted
                    config[secret_name] = load_secret(secret_name)
                    logger.info(f"Loaded unencrypted secret: {secret_name}")
            else:
                config[secret_name] = load_secret(secret_name)
                logger.info(f"Loaded secret: {secret_name}")
        except ValueError as e:
            logger.warning(f"Missing secret: {secret_name} - {e}")
            config[secret_name] = None
    
    return config


def check_secrets_status() -> dict:
    """
    Check the status of all required secrets
    
    Returns:
        Dictionary with secret status information
    """
    required_secrets = [
        'SEPOLIA_RPC_URL',
        'SERVICE_PRIVATE_KEY', 
        'BASIC_TRANSPARENCY_CONTRACT_ADDRESS',
        'CARE_TOKEN_CONTRACT_ADDRESS',
        'TESTIMONY_NFT_CONTRACT_ADDRESS',
        'BASIC_TRANSPARENCY_ABI_JSON',
        'CARE_TOKEN_ABI_JSON',
        'TESTIMONY_NFT_ABI_JSON'
    ]
    
    status = {
        'configured': [],
        'missing': [],
        'total_required': len(required_secrets)
    }
    
    for secret_name in required_secrets:
        if os.getenv(secret_name):
            status['configured'].append(secret_name)
        else:
            status['missing'].append(secret_name)
    
    status['configured_count'] = len(status['configured'])
    status['missing_count'] = len(status['missing'])
    status['is_ready'] = status['missing_count'] == 0
    
    return status


if __name__ == "__main__":
    # Test the secrets utility
    print("Grain Sigil Secrets Utility")
    print("=" * 40)
    
    status = check_secrets_status()
    print(f"Configured secrets: {status['configured_count']}/{status['total_required']}")
    
    if status['missing']:
        print("Missing secrets:")
        for secret in status['missing']:
            print(f"  - {secret}")
    
    if status['is_ready']:
        print("✓ All secrets configured!")
    else:
        print("⚠ Some secrets missing - check Replit Secrets panel")