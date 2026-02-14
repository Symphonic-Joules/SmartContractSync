import logging
from flask import Blueprint, request, jsonify, render_template
from models import GrainSigilMetadata, AccessPolicy, DigitalLockConfig, OnChainAction, WalletView, NftAsset
from blockchain_service import blockchain_service
from app import db
from database_models import Sigil, Lock, AccessLog

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')


@main_bp.route('/sigil-creator')
def sigil_creator():
    """Sigil creation interface"""
    return render_template('sigil_creator.html')


@main_bp.route('/access-control')
def access_control():
    """Access control interface"""
    return render_template('access_control.html')


@main_bp.route('/wallet-view')
def wallet_view():
    """Wallet view interface"""
    return render_template('wallet_view.html')


@main_bp.route('/api/create-sigil', methods=['POST'])
def create_sigil():
    """Create a new Grain Sigil"""
    try:
        data = request.json or {}

        # Create sigil metadata
        sigil_metadata = GrainSigilMetadata(
            identity_proof_hash=data.get('identity_proof_hash', ''),
            ethical_profile=data.get('ethical_declarations', []),
            capabilities=data.get('capabilities', []),
            user_attributes=data.get('user_attributes', {}),
            proofs=data.get('proofs', {}),
            linked_wallet_address=data.get('linked_wallet_address', ''),
            sigil_fingerprint=data.get('sigil_fingerprint'),
            verifiable_credentials=data.get('verifiable_credentials', []))

        # Generate fingerprint if not provided
        if not sigil_metadata.sigil_fingerprint:
            sigil_metadata.sigil_fingerprint = blockchain_service.generate_sigil_fingerprint(
                sigil_metadata.to_dict())

        # Create database record
        db_sigil = Sigil.from_metadata(sigil_metadata.to_dict(),
                                       sigil_metadata.sigil_fingerprint)
        db.session.add(db_sigil)
        db.session.commit()

        logger.info(
            f"Created sigil with fingerprint: {sigil_metadata.sigil_fingerprint}"
        )

        return jsonify({
            "status": "success",
            "sigil_fingerprint": sigil_metadata.sigil_fingerprint,
            "metadata": sigil_metadata.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating sigil: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@main_bp.route('/api/create-lock', methods=['POST'])
def create_lock():
    """Create a new digital lock"""
    try:
        data = request.json or {}

        # Parse access policy
        access_policy_data = data.get('access_policy', {})
        access_policy = AccessPolicy(
            required_ethics=access_policy_data.get('required_ethics', []),
            required_capabilities=access_policy_data.get(
                'required_capabilities', []),
            attribute_conditions=access_policy_data.get(
                'attribute_conditions', {}),
            requires_proof_type=access_policy_data.get('requires_proof_type'),
            required_credentials=access_policy_data.get(
                'required_credentials', []))

        # Parse on-chain actions
        on_chain_actions = []
        for action_data in data.get('on_chain_actions', []):
            on_chain_actions.append(
                OnChainAction(function=action_data['function'],
                              params=action_data['params']))

        # Create lock config
        lock_config = DigitalLockConfig(type=data.get('type',
                                                      'access_control'),
                                        controls=data.get('controls', ''),
                                        access_policy=access_policy,
                                        access_message=data.get(
                                            'access_message', ''),
                                        on_chain_actions=on_chain_actions)

        # Generate lock ID
        lock_id = blockchain_service.generate_sigil_fingerprint(
            lock_config.to_dict())

        # Create database record
        db_lock = Lock.from_config(lock_config.to_dict(), lock_id)
        db.session.add(db_lock)
        db.session.commit()

        logger.info(f"Created lock with ID: {lock_id}")

        return jsonify({
            "status": "success",
            "lock_id": lock_id,
            "lock_config": lock_config.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating lock: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@main_bp.route('/api/check-access', methods=['POST'])
def check_access():
    """Check access against a digital lock"""
    try:
        data = request.json or {}
        sigil_fingerprint = data.get('sigil_fingerprint')
        lock_id = data.get('lock_id')

        if not sigil_fingerprint or not lock_id:
            return jsonify({
                "status": "error",
                "message": "Missing sigil_fingerprint or lock_id"
            }), 400

        # Get sigil and lock from database
        sigil = Sigil.query.filter_by(
            sigil_fingerprint=sigil_fingerprint).first()
        lock = Lock.query.filter_by(lock_id=lock_id).first()

        if not sigil:
            return jsonify({
                "status": "error",
                "message": "Sigil not found"
            }), 404

        if not lock:
            return jsonify({
                "status": "error",
                "message": "Lock not found"
            }), 404

        # Check access policy
        access_granted, message = blockchain_service.check_access_policy(
            sigil.to_dict(), lock.access_policy)

        transaction_receipts = []
        current_contract_state = {}

        # Execute on-chain actions if access is granted
        if access_granted and lock.on_chain_actions:
            for action_data in lock.on_chain_actions:
                try:
                    action = OnChainAction(function=action_data['function'],
                                           params=action_data['params'])

                    if action.function == "allocate_reparations":
                        result = blockchain_service.allocate_reparations(
                            sigil.linked_wallet_address, action.params[0])
                        transaction_receipts.append(result)
                    elif action.function == "mint_testimony_credit":
                        result = blockchain_service.mint_testimony_credit(
                            sigil.linked_wallet_address, action.params[0])
                        transaction_receipts.append(result)
                    elif action.function == "mint_creative_work":
                        result = blockchain_service.mint_creative_work(
                            sigil.linked_wallet_address, action.params[0])
                        transaction_receipts.append(result)
                    elif action.function == "update_reputation":
                        result = blockchain_service.update_reputation(
                            sigil.linked_wallet_address, action.params[0],
                            action.params[1])
                        transaction_receipts.append(result)
                except Exception as e:
                    logger.error(
                        f"Error executing on-chain action {action_data.get('function', 'unknown')}: {e}"
                    )
                    transaction_receipts.append({
                        "status":
                        "error",
                        "action":
                        action_data.get('function', 'unknown'),
                        "error":
                        str(e)
                    })

        # Log access attempt
        access_log = AccessLog(sigil_fingerprint=sigil_fingerprint,
                               lock_id=lock_id,
                               access_granted=access_granted,
                               message=message,
                               transaction_receipts=transaction_receipts)
        db.session.add(access_log)
        db.session.commit()

        return jsonify({
            "access_granted": access_granted,
            "message": message,
            "transaction_receipts": transaction_receipts,
            "current_contract_state": current_contract_state,
            "sigil_metadata": sigil.to_dict(),
            "lock_details": lock.to_dict()
        })

    except Exception as e:
        logger.error(f"Error checking access: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@main_bp.route('/api/wallet/<wallet_address>')
def get_wallet_assets(wallet_address):
    """Get wallet assets"""
    try:
        assets = blockchain_service.get_wallet_assets(wallet_address)
        return jsonify(assets)
    except Exception as e:
        logger.error(f"Error getting wallet assets: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@main_bp.route('/api/sigils')
def list_sigils():
    """List all created sigils"""
    try:
        sigils = Sigil.query.all()
        return jsonify(
            {sigil.sigil_fingerprint: sigil.to_dict()
             for sigil in sigils})
    except Exception as e:
        logger.error(f"Error listing sigils: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@main_bp.route('/api/locks')
def list_locks():
    """List all created locks"""
    try:
        locks = Lock.query.all()
        return jsonify({lock.lock_id: lock.to_dict() for lock in locks})
    except Exception as e:
        logger.error(f"Error listing locks: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@main_bp.route('/api/blockchain-status')
def blockchain_status():
    """Get blockchain connection status"""
    try:
        status = {
            "connected":
            blockchain_service.w3.is_connected(),
            "block_number":
            blockchain_service.w3.eth.block_number
            if blockchain_service.w3.is_connected() else None,
            "service_account":
            blockchain_service.service_account.address
            if blockchain_service.service_account else None,
            "contracts": {
                "basic_transparency":
                blockchain_service.BASIC_TRANSPARENCY_CONTRACT_ADDRESS,
                "care_token": blockchain_service.CARE_TOKEN_CONTRACT_ADDRESS,
                "testimony_nft":
                blockchain_service.TESTIMONY_NFT_CONTRACT_ADDRESS
            }
        }
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting blockchain status: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
