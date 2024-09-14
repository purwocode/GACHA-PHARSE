import binascii
import time
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum, Bip39Languages
from tqdm import tqdm

def generate_bep20_wallet():
    while True:
        # Generate a random mnemonic
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
        
        # Generate seed from mnemonic
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        
        # Generate BIP44 master key
        bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BINANCE_SMART_CHAIN)
        
        # Derive BIP44 chain node
        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
        bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
        
        # Derive address key
        bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)
        
        # Get address public key
        address = bip44_addr_ctx.PublicKey().ToAddress()
        
        # Get private key
        private_key = binascii.hexlify(bip44_addr_ctx.PrivateKey().Raw().ToBytes()).decode()
        
        return {
            "mnemonic": mnemonic,
            "private_key": private_key,
            "address": address
        }

def main():
    # Meminta input dari pengguna
    num_wallets = int(input("Mau Buat Berapa Wallet? "))
    file_name = input("Simpan Hasil Dengan Nama? ")

    # Memastikan file name berakhir dengan .txt
    if not file_name.endswith('.txt'):
        file_name += '.txt'

    # Set untuk menyimpan address yang sudah dibuat
    created_addresses = set()

    # Membuat wallet sesuai jumlah yang diminta dan menyimpan ke file
    with open(file_name, 'w') as f:
        wallet_count = 0
        pbar = tqdm(total=num_wallets, desc="Generating Wallets", unit="wallet")
        while wallet_count < num_wallets:
            start_time = time.time()
            wallet = generate_bep20_wallet()
            
            # Memeriksa apakah address sudah ada
            if wallet['address'] not in created_addresses:
                created_addresses.add(wallet['address'])
                wallet_count += 1
                f.write(f"{wallet['mnemonic']}|{wallet['private_key']}|{wallet['address']}\n")
                
                # Menghitung waktu yang diperlukan
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # Update progress bar
                pbar.update(1)
                pbar.set_postfix({"Time": f"{elapsed_time:.2f}s"})
            else:
                pbar.write("Duplikat ditemukan, membuat wallet baru...")

        pbar.close()

    print(f"\nHasil telah disimpan dalam file: {file_name}")

if __name__ == "__main__":
    main()