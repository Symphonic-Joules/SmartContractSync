#!/usr/bin/env python3
"""
🛡️ Grain Sigil Secrets Encryption Utility
Encrypt sensitive values for safe storage in Replit Secrets
"""
from secrets_util import encode_for_env, check_secrets_status

def encrypt_for_replit():
    """Interactive encryption tool for Replit Secrets"""
    print("🛡️ Grain Sigil Secrets Encryption Utility")
    print("=" * 50)
    print("Encrypt sensitive values for safe storage in Replit Secrets")
    print()
    
    # List of secrets that should be encrypted
    sensitive_secrets = {
        "SEPOLIA_RPC_URL": "Your Infura/Alchemy Sepolia endpoint",
        "SERVICE_PRIVATE_KEY": "Your wallet's private key (no 0x prefix)"
    }
    
    # List of secrets that can be stored plain
    plain_secrets = {
        "BASIC_TRANSPARENCY_CONTRACT_ADDRESS": "Contract address (0x...)",
        "CARE_TOKEN_CONTRACT_ADDRESS": "Contract address (0x...)", 
        "TESTIMONY_NFT_CONTRACT_ADDRESS": "Contract address (0x...)",
        "BASIC_TRANSPARENCY_ABI_JSON": "Minified ABI JSON string",
        "CARE_TOKEN_ABI_JSON": "Minified ABI JSON string",
        "TESTIMONY_NFT_ABI_JSON": "Minified ABI JSON string"
    }
    
    print("📋 ENCRYPTED SECRETS (recommended for sensitive data):")
    print("-" * 50)
    for secret, desc in sensitive_secrets.items():
        print(f"• {secret}")
        print(f"  {desc}")
        value = input(f"  Enter value (empty to skip): ").strip()
        if value:
            encrypted = encode_for_env(value)
            print(f"  🔐 Encrypted: {encrypted}")
            print(f"  ➡️  Add to Replit Secrets: {secret} = {encrypted}")
        print()
    
    print("📄 PLAIN SECRETS (can be stored unencrypted):")
    print("-" * 50)
    for secret, desc in plain_secrets.items():
        print(f"• {secret}: {desc}")
    print()
    
    print("✅ SETUP COMPLETE!")
    print("Next steps:")
    print("1. Copy the encrypted values above")
    print("2. Open Replit Secrets (🔒 icon in sidebar)")
    print("3. Add each key-value pair")
    print("4. Your app will automatically restart and connect to Sepolia!")
    print()
    print("Your app code will automatically decrypt with:")
    print("  private_key = load_secret('SERVICE_PRIVATE_KEY', key='Grain')")
    print("  rpc_url = load_secret('SEPOLIA_RPC_URL', key='Grain')")

def quick_encrypt():
    """Quick encrypt mode for single values"""
    print("🔐 Quick Encrypt Mode")
    print("Enter a value to encrypt with the 'Grain' key:")
    value = input("Value: ").strip()
    if value:
        encrypted = encode_for_env(value)
        print(f"Encrypted: {encrypted}")
        print("Copy this encrypted value to your Replit Secret")
    else:
        print("No value provided.")

def check_current_status():
    """Check current secrets configuration"""
    print("📊 Current Secrets Status")
    print("-" * 30)
    status = check_secrets_status()
    
    print(f"Configured: {status['configured_count']}/{status['total_required']}")
    
    if status['configured']:
        print("✅ Configured secrets:")
        for secret in status['configured']:
            print(f"  • {secret}")
    
    if status['missing']:
        print("❌ Missing secrets:")
        for secret in status['missing']:
            print(f"  • {secret}")
    
    if status['is_ready']:
        print("\n🎉 All secrets configured! Your app is ready for Sepolia.")
    else:
        print(f"\n⚠️  {status['missing_count']} secrets still needed.")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Full setup (encrypt sensitive secrets)")
    print("2. Quick encrypt (single value)")
    print("3. Check current status")
    
    choice = input("Enter choice (1-3): ").strip()
    print()
    
    if choice == "1":
        encrypt_for_replit()
    elif choice == "2":
        quick_encrypt()
    elif choice == "3":
        check_current_status()
    else:
        print("Invalid choice. Running status check...")
        check_current_status()