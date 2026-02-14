#!/usr/bin/env python3
"""
Example usage of the secure secrets utility
Shows exactly how to use encrypted secrets as shown in your code snippet
"""
from secrets_util import load_secret, encrypt_secret

def demonstrate_your_example():
    """Demonstrates your exact code pattern"""
    print("=== Your Example Usage Pattern ===")
    print("from secrets_util import load_secret")
    print()
    print("# Decode your key safely from environment")
    print('my_key = load_secret("MY_ENCRYPTED_KEY", key="Grain")')
    print('print(f"Decrypted key: {my_key}")')
    print()
    
    try:
        # Decode your key safely from environment
        my_key = load_secret("MY_ENCRYPTED_KEY", key="Grain")
        print(f"Decrypted key: {my_key}")
    except ValueError as e:
        print(f"Result: {e}")
        print("\nTo use this pattern:")
        print("1. Encrypt your secret: encrypt_secret('your_secret_value', 'Grain')")
        print("2. Store the encrypted result in Replit Secrets as MY_ENCRYPTED_KEY")
        print("3. The load_secret function will automatically decrypt it")

def show_encryption_example():
    """Show how to prepare an encrypted secret for storage"""
    print("\n=== How to Prepare Encrypted Secrets ===")
    
    # Example: encrypt a private key
    example_private_key = "your_actual_private_key_here"
    encrypted_key = encrypt_secret(example_private_key, "Grain")
    
    print(f"Original: {example_private_key}")
    print(f"Encrypted: {encrypted_key}")
    print()
    print("Steps to use:")
    print("1. Run this script to encrypt your actual secret")
    print("2. Copy the encrypted result")
    print("3. In Replit Secrets, set MY_ENCRYPTED_KEY = <encrypted_result>")
    print("4. Your app code: my_key = load_secret('MY_ENCRYPTED_KEY', key='Grain')")

def show_blockchain_secrets_setup():
    """Show how to set up all required blockchain secrets"""
    print("\n=== Blockchain Secrets Setup ===")
    print("Required secrets for Sepolia connection:")
    
    required = [
        ("SEPOLIA_RPC_URL", "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"),
        ("SERVICE_PRIVATE_KEY", "your_test_account_private_key"),
        ("BASIC_TRANSPARENCY_CONTRACT_ADDRESS", "0x1234..."),
        ("CARE_TOKEN_CONTRACT_ADDRESS", "0x5678..."),
        ("TESTIMONY_NFT_CONTRACT_ADDRESS", "0x9abc..."),
        ("BASIC_TRANSPARENCY_ABI_JSON", '[{"inputs":[],...}]'),
        ("CARE_TOKEN_ABI_JSON", '[{"inputs":[],...}]'),
        ("TESTIMONY_NFT_ABI_JSON", '[{"inputs":[],...}]')
    ]
    
    for name, example in required:
        print(f"  {name} = {example}")
    
    print("\nFor encrypted storage (optional):")
    print("  - Encrypt sensitive values with encrypt_secret(value, 'Grain')")
    print("  - Store encrypted result in Replit Secrets")
    print("  - Use load_secret(name, key='Grain') to decrypt")

if __name__ == "__main__":
    demonstrate_your_example()
    show_encryption_example()
    show_blockchain_secrets_setup()