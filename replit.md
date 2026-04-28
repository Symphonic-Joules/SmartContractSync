# Grain Sigil Autonomy Network

## Overview

The Grain Sigil Autonomy Network is a decentralized identity and access control system built on blockchain technology. It provides a survivor-led autonomy network that enables users to create digital identity "sigils" (credentials) and manage access control through blockchain-based smart contracts. The system combines Flask backend services with Web3 integration for Ethereum testnet interactions.

## System Architecture

### Frontend Architecture
- **Templates**: Server-side rendered HTML pages using Jinja2 templating
- **Static Assets**: CSS and JavaScript files for client-side functionality
- **Bootstrap Framework**: Dark theme UI components with custom styling
- **Web3 Integration**: Client-side blockchain interactions through MetaMask

### Backend Architecture
- **Flask Application**: Lightweight Python web framework
- **Blueprint Structure**: Modular route organization
- **CORS Enabled**: Cross-origin resource sharing for API access
- **Proxy Middleware**: Production-ready request handling

### Data Models
- **GrainSigilMetadata**: Digital identity credential structure
- **AccessPolicy**: Access control rule definitions
- **Dataclass Pattern**: Type-safe data structures with validation

## Key Components

### 1. Identity Management (Grain Sigils)
- **Purpose**: Create and manage decentralized identity credentials
- **Features**: Ethical profiles, capabilities, user attributes, verifiable credentials
- **Implementation**: Metadata stored as JSON with blockchain anchoring

### 2. Blockchain Service Layer
- **Web3.py Integration**: Direct interaction with Ethereum Sepolia testnet
- **Smart Contract Support**: 
  - Basic Transparency Contract
  - Care Token (ERC-20)
  - Testimony NFT (ERC-721)
- **Service Account**: Automated transaction signing for system operations

### 3. Access Control System
- **Digital Locks**: Blockchain-based access restrictions
- **Policy Engine**: Rule-based access management
- **Wallet Integration**: MetaMask connectivity for user authentication

### 4. User Interface
- **Dashboard**: Central hub for system overview
- **Sigil Creator**: Interactive identity credential builder
- **Access Control**: Lock creation and management interface
- **Wallet View**: Asset and credential viewer

## Data Flow

1. **Identity Creation**: Users create sigils through the web interface
2. **Blockchain Anchoring**: Sigil metadata is hashed and stored on-chain
3. **Access Control**: Digital locks are created with specific access policies
4. **Verification**: Third parties can verify credentials through blockchain queries
5. **Asset Management**: Users view their digital assets through wallet interface

## External Dependencies

### Blockchain Infrastructure
- **Sepolia Testnet**: Ethereum test network for development
- **Web3.py**: Python library for Ethereum interaction
- **MetaMask**: Browser wallet for user transactions

### Development Stack
- **Flask**: Python web framework
- **Bootstrap**: Frontend UI framework
- **Font Awesome**: Icon library
- **CORS**: Cross-origin request handling

### Environment Variables
- `SEPOLIA_RPC_URL`: Ethereum node endpoint
- `SERVICE_PRIVATE_KEY`: System account private key
- `*_CONTRACT_ADDRESS`: Smart contract addresses
- `*_ABI_JSON`: Contract interface definitions

## Deployment Strategy

### Development Environment
- **Local Flask Server**: Debug mode on port 5000
- **PostgreSQL Database**: Persistent storage with SQLAlchemy ORM
- **Environment Variables**: `.env` file configuration

### Production Considerations
- **Database Scaling**: PostgreSQL optimization and connection pooling
- **Security Hardening**: Secure private key management
- **Load Balancing**: Multiple Flask instances behind proxy
- **SSL/TLS**: HTTPS encryption for all endpoints

### Smart Contract Deployment
- **Testnet First**: Sepolia deployment for testing
- **Mainnet Migration**: Production deployment to Ethereum mainnet
- **Contract Verification**: Public source code verification

## Authentication

Replit Auth is integrated via `replit_auth.py` using OpenID Connect (flask-dance + flask-login).

- `User` and `OAuth` models live in `database_models.py` (tables: `users`, `flask_dance_oauth`)
- Use `@require_login` decorator on any route that needs authentication
- `current_user` (flask-login) is available in all templates
- Login flow: `/auth/login` → OAuth → callback → save user → redirect
- Logout: `/auth/logout` (clears session + Replit OIDC end-session)
- Protected routes: `/sigil-creator`, `/access-control`, `/wallet-view`
- Home (`/`) shows a landing page for logged-out users and the dashboard for logged-in users

## Changelog
- April 28, 2026: Added Replit Auth
  - Integrated flask-dance + flask-login via OpenID Connect
  - User and OAuth models added to database
  - Protected sigil-creator, access-control, wallet-view routes
  - Landing page for logged-out users; dashboard for logged-in users
  - Avatar, display name, and logout button in all navbars
- June 30, 2025: Initial setup and complete implementation
  - Fixed web3.py compatibility issues for modern library versions
  - Implemented full Flask application with blockchain integration
  - Created complete UI with sigil creation, access control, and wallet viewing
  - Added robust error handling and fallback mechanisms
  - Successfully deployed and tested all core functionality
- June 30, 2025: Database integration completed
  - Added PostgreSQL database with SQLAlchemy ORM
  - Created database models for Sigils, Locks, and AccessLogs
  - Migrated from in-memory storage to persistent database storage
  - All CRUD operations now use database transactions
  - Verified database functionality with test data
- June 30, 2025: Bug fixes and demo mode implementation
  - Fixed critical startup crashes and import issues
  - Resolved database model type checking errors
  - Added automatic demo mode when blockchain secrets missing
  - All application features now work with mock data until real secrets added
  - Application successfully runs without external dependencies

## User Preferences

Preferred communication style: Simple, everyday language.