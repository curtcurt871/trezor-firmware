from trezor.messages.StellarAddress import StellarAddress
from trezor.messages.StellarGetAddress import StellarGetAddress
from trezor.ui.layouts import show_address

from apps.common import paths, seed
from apps.common.keychain import auto_keychain

from . import helpers


@auto_keychain(__name__)
async def get_address(ctx, msg: StellarGetAddress, keychain):
    await paths.validate_path(ctx, keychain, msg.address_n)

    node = keychain.derive(msg.address_n)
    pubkey = seed.remove_ed25519_prefix(node.public_key())
    address = helpers.address_from_public_key(pubkey)

    if msg.show_display:
        title = paths.address_n_to_str(msg.address_n)
        await show_address(
            ctx, address=address, address_qr=address.upper(), title=title
        )

    return StellarAddress(address=address)
