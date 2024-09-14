from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from web3 import Web3

def create_bep20_wallet(mnemonic):
    # Generate seed from mnemonic
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    # Create BIP44 object for Binance Smart Chain (BSC uses the same derivation path as Ethereum)
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)

    # Derive the first account
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)

    # Derive the external chain
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

    # Derive the first address index
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)

    # Get the private key and public address
    priv_key = bip44_addr_ctx.PrivateKey().Raw().ToBytes()
    pub_address = Web3.to_checksum_address(bip44_addr_ctx.PublicKey().ToAddress())

    return {
        'private_key': priv_key.hex(),
        'public_address': pub_address
    }

def is_valid_mnemonic_length(words):
    return len(words) in [12, 15, 18, 21, 24]

def get_valid_filename(prompt):
    while True:
        filename = input(prompt).strip()
        if filename:
            return filename
        print("Nama file tidak boleh kosong. Silakan coba lagi.")

def main():
    print("Selamat datang di pembuat dompet BEP20!")
    
    # Meminta input nama file dari pengguna tanpa nilai default
    input_file = get_valid_filename("Masukkan nama file input: ")
    output_file = get_valid_filename("Masukkan nama file output: ")
    
    print(f"Memproses mnemonic dari file {input_file}...")

    try:
        with open(input_file, 'r') as mnemonic_file, open(output_file, 'w') as wallet_file:
            for line in mnemonic_file:
                mnemonic = line.strip()
                words = mnemonic.split()
                
                if not is_valid_mnemonic_length(words):
                    print(f"[-] Invalid Mnemonic '{mnemonic[:20]}...' (Not 12, 15, 18, 21, atau 24 Word)")
                    continue
                
                try:
                    wallet = create_bep20_wallet(mnemonic)
                    wallet_file.write(f"{mnemonic}|{wallet['private_key']}|{wallet['public_address']}\n")
                    print(f"[+] Success : {mnemonic[:20]}... ({len(words)} kata)")
                except Exception as e:
                    print(f"[-] Error '{mnemonic[:20]}...'")

        print(f"\nPembuatan dompet selesai. Hasil disimpan di {output_file}")
        print("PERINGATAN: Jangan pernah membagikan kunci privat Anda kepada siapa pun!")
    except FileNotFoundError:
        print(f"[-] File {input_file} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan")

if __name__ == "__main__":
    main()