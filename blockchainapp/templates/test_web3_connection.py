#!/usr/bin/env python3
"""
Test your Web3 connection pattern for the Grain Sigil app
"""

from web3 import Web3
from secrets_util import load_secret, SecretError

try:
    # Your exact pattern from the message
    rpc_url = load_secret("SEPOLIA_RPC_URL", key="Grain")
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if w3.is_connected():
        print("✅ Connected to Sepolia! ✨")
        block = w3.eth.get_block("latest")  # Get the latest block if connected
        print(f"Current block number: {block.number}")
        print(f"Gas limit: {block.gasLimit:,}")
    else:
        print("❌ Could not connect to Sepolia. Please check your RPC URL and secrets.")

except SecretError as e:
    print(f"❌ Secret loading error: {e}")
    print("💡 To fix this:")
    print("1. Get your Alchemy API key from alchemy.com")
    print("2. Encrypt it: python -c \"from secrets_util import encode_for_env; print(encode_for_env('YOUR_ALCHEMY_URL'))\"")
    print("3. Add encrypted value to Replit Secrets as 'SEPOLIA_RPC_URL'")
    
except Exception as e:
    print(f"❌ Connection error: {e}")