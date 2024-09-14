from web3 import Web3

# Setup connection to BSC
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

# Check connection
print(web3.is_connected())

# Token contract addresses
BUSD_ADDRESS = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'  # BUSD
USDT_ADDRESS = '0x55d398326f99059fF775485246999027B3197955'  # USDT

# ABI for ERC20 tokens
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]

# Create contract instances
busd_contract = web3.eth.contract(address=BUSD_ADDRESS, abi=ERC20_ABI)
usdt_contract = web3.eth.contract(address=USDT_ADDRESS, abi=ERC20_ABI)

# Get input and output file names from user
input_file = input("Enter the name of the input file (default: listwallet.txt): ") or "listwallet.txt"
output_file = input("Enter the name of the output file for non-zero balances (default: results.txt): ") or "results.txt"
zero_balance_file = input("Enter the name of the output file for zero balances (default: walletzero.txt): ") or "walletzero.txt"

# Read addresses from input file
with open(input_file, 'r') as file:
    lines = file.readlines()

# Process addresses and write results immediately
for line in lines:
    parts = line.strip().split('|')
    if len(parts) != 3:
        print(f"Invalid line format: {line}")
        continue
    
    phrase, key, address = parts
    if not Web3.is_checksum_address(address):
        print(f"Invalid address: {address}")
        continue
    
    bnb_balance = web3.eth.get_balance(address)
    busd_balance = busd_contract.functions.balanceOf(address).call()
    usdt_balance = usdt_contract.functions.balanceOf(address).call()

    bnb_balance_ether = web3.from_wei(bnb_balance, 'ether')
    busd_balance_ether = web3.from_wei(busd_balance, 'ether')
    usdt_balance_ether = web3.from_wei(usdt_balance, 'ether')

    if bnb_balance > 0 or busd_balance > 0 or usdt_balance > 0:
        # File output (unchanged)
        file_result = f"[{phrase}] [{key}] [{address}] => BNB: [{bnb_balance_ether:.18f}], BUSD: [{busd_balance_ether:.18f}], USDT: [{usdt_balance_ether:.18f}]\n"
        with open(output_file, 'a') as result_file:
            result_file.write(file_result)
        
        # Console output (modified)
        console_result = f"[+] [{address}] => BNB: [{bnb_balance_ether:.18f}], BUSD: [{busd_balance_ether:.18f}], USDT: [{usdt_balance_ether:.18f}]"
        print(console_result)
    else:
        # File output (unchanged)
        with open(zero_balance_file, 'a') as zero_file:
            zero_file.write(f"[{phrase}] [{key}] [{address}]\n")
        
        # Console output (modified)
        print(f"[-] [Zero Balance] => {address}")

print("Finished checking addresses.")