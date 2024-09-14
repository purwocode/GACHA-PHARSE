import os

print("Welcome to CrackLog Silakan Pilih Menu:")
print(f"[1] Generate Mnemonic+PrivKey+Address")
print(f"[2] Make PrivKey+Wallet Form  Mnemonic")
print(f"[3] Check Balance USDT|BUSD|BNB")

def screen_clear():
    os.system('cls')

data = {
    '1':'generate.py',
    '2':'generateformfile.py',
    '3':'checkbalance.py',
}

SCRIPT_DIR = "Scripts"

pilihan = input("Pilih Angka 1/2/3: ")
if data.get(pilihan):
    full_path = os.path.join(SCRIPT_DIR, data.get(pilihan))
    os.system(f'python {full_path}')
else:
    print('ga ada ')