#!/usr/bin/env python3
"""
Test script for the secrets utility
Demonstrates the encrypted secrets functionality
"""
from secrets_util import load_secret, encrypt_secret, decrypt_secret, check_secrets_status

def test_encryption():
    """Test the encryption/decryption functionality"""
    print("Testing encryption/decryption...")
    
    # Test secret
    original_secret = "test_private_key_12345"
    key = "Grain"
    
    # Encrypt
    encrypted = encrypt_secret(original_secret, key)
    print(f"Original: {original_secret}")
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = decrypt_secret(encrypted, key)
    print(f"Decrypted: {decrypted}")
    
    assert original_secret == decrypted, "Encryption/decryption failed!"
    print("✓ Encryption/decryption test passed!")

def test_your_example():
    """Test your specific example usage"""
    print("\nTesting your example usage pattern...")
    
    try:
        # Simulate your example
        my_key = load_secret("MY_ENCRYPTED_KEY", key="Grain")
        print(f"Decrypted key: {my_key}")
    except ValueError as e:
        print(f"Expected error (secret not set): {e}")

def main():
    print("=== Grain Sigil Secrets Utility Test ===")
    
    # Test encryption
    test_encryption()
    
    # Test your example
    test_your_example()
    
    # Check current secrets status
    print("\n=== Current Secrets Status ===")
    status = check_secrets_status()
    print(f"Configured: {status['configured_count']}/{status['total_required']}")
    
    if status['missing']:
        print("Missing secrets:")
        for secret in status['missing']:
            print(f"  - {secret}")
    
    if status['is_ready']:
        print("✓ All secrets configured!")
    else:
        print("⚠ Add missing secrets to Replit Secrets panel")

if __name__ == "__main__":
    main()