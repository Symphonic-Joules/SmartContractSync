#!/usr/bin/env python3
"""
Test script to verify Alchemy connection setup for Grain Sigil app
Run this after adding your real Alchemy secrets to test connectivity
"""

def test_alchemy_connection():
    """Test the Alchemy connection with your setup"""
    try:
        from secrets_util import load_secret
        from web3 import Web3
        
        print("🧪 Testing Alchemy Connection...")
        print("-" * 40)
        
        # Try to load encrypted secret
        try:
            ALCHEMY_URL = load_secret("SEPOLIA_RPC_URL", key="Grain")
            print("✅ Successfully loaded SEPOLIA_RPC_URL from encrypted secret")
        except Exception as e:
            print(f"❌ Failed to load SEPOLIA_RPC_URL: {e}")
            return False
        
        # Test Web3 connection
        w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
        
        if w3.is_connected():
            print("✅ Connected to Sepolia Testnet via Alchemy!")
            
            # Get latest block
            try:
                block = w3.eth.get_block("latest")
                print(f"🔍 Latest Block: #{block['number']}")
                print(f"⛽ Gas Limit: {block['gasLimit']:,}")
                print(f"📅 Timestamp: {block['timestamp']}")
                
                return True
                
            except Exception as e:
                print(f"❌ Error fetching block data: {e}")
                return False
        else:
            print("❌ Connection failed - check your RPC URL")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_setup_instructions():
    """Show instructions for setting up Alchemy"""
    print("\n📋 To set up Alchemy connection:")
    print("1. Go to alchemy.com and create a free account")
    print("2. Create a new app for 'Ethereum Sepolia'") 
    print("3. Copy your HTTP URL (looks like: https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY)")
    print("4. Encrypt it using: python encrypt_secrets.py")
    print("5. Add the encrypted value to Replit Secrets as 'SEPOLIA_RPC_URL'")
    print("\nYour app will automatically switch from demo mode to live blockchain!")

if __name__ == "__main__":
    success = test_alchemy_connection()
    
    if not success:
        show_setup_instructions()
    else:
        print("\n🎉 Connection successful! Your app is ready for live blockchain features.")