import time
from web3 import Web3
from tenacity import retry, wait_fixed
from pathlib import Path
import pydash as _

ETH_NODE_URL = 'https://mainnet.infura.io/v3/38c9ff19cffc4c958c4fc12f2b88c2de'

@retry(wait=wait_fixed(2), stop=3)
def connect_web3():
    return Web3(Web3.HTTPProvider(ETH_NODE_URL))

def watch_blocks():
    w3 = connect_web3()
    last_block = w3.eth.block_number
    while True:
        current_block = w3.eth.block_number
        if current_block > last_block:
            block = w3.eth.get_block(current_block, full_transactions=True)
            for tx in block.transactions:
                print({
                    'hash': tx.hash.hex(),
                    'from': tx['from'],
                    'to': tx.get('to'),
                    'value_eth': w3.from_wei(tx['value'], 'ether')
                })
            last_block = current_block
        time.sleep(2)

if __name__ == '__main__':
    watch_blocks()
