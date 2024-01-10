from typing import Optional

import openpyxl
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic

# Number of wallets
N = int(input("Enter number of wallets: "))
# folder path
path = str(input("Enter the folder path for xlsx: "))

wallets = []

for i in range(N):
    MNEMONIC: str = generate_mnemonic(language="english", strength=256)
    PASSPHRASE: Optional[str] = None

    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    bip44_hdwallet.clean_derivation()
    bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=0
    )
    bip44_hdwallet.from_path(path=bip44_derivation)
    wallets.append(
        {
            "Mnemonic": bip44_hdwallet.mnemonic(),
            "Address": bip44_hdwallet.address(),
            "Private key": bip44_hdwallet.private_key(),
        }
    )
    bip44_hdwallet.clean_derivation()

book = openpyxl.Workbook()
sheet = book.active
sheet.append(["Mnemonic", "Address", "Private key"])

for wallet in wallets:
    sheet.append([wallet["Mnemonic"], wallet["Address"], wallet["Private key"]])

book.save(f"{path}/wallets.xlsx")
book.close()
