from typing import Optional
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
import openpyxl

book = openpyxl.Workbook()
sheet = book.active
sheet['A1'] = "Mnemonic"
sheet['B1'] = "Address"
sheet['C1'] = "Private key"

# Number of wallets
N = int(input("Enter number of wallets: "))
path = str(input("Enter the folder path for csv: "))

for i in range(N):
    MNEMONIC: str = generate_mnemonic(language="english", strength=128)
    PASSPHRASE: Optional[str] = None

    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    bip44_hdwallet.clean_derivation()
    sheet.cell(row=i + 2, column=1).value = bip44_hdwallet.mnemonic()
    bip44_derivation: BIP44Derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet, account=0, change=False, address=0
    )
    bip44_hdwallet.from_path(path=bip44_derivation)
    sheet.cell(row=i + 2, column=2).value = bip44_hdwallet.address()
    sheet.cell(row=i + 2, column=3).value = bip44_hdwallet.private_key()
    bip44_hdwallet.clean_derivation()

book.save(f"{path}/wallets.xlsx")
book.close()
