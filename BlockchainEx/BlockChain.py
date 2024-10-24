import datetime
import hashlib
from colorama import init
init()
from colorama import Fore, Back, Style
blockNoToEdit = 4

class Block:

    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0

    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data


    def hash(self):

        h = hashlib.sha256()

        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )

        return h.hexdigest()


    def __str__(self):

        return ("Block Hash: "
                + str(self.hash())
                + "\nPreviousHash: "
                + str(self.previous_hash)
                + "\nBlockNo: " + str(self.blockNo)
                + "\nBlock Data: " + str(self.data)
                + "\nHashes: " + str(self.nonce)
                + "\n--------------")

class Blockchain:

    diff = 10

    maxNonce = 2**32

    target = 2 ** (256-diff)

    block = Block("Genesis")

    head = block

    def add(self, block):

        block.previous_hash = self.block.hash()

        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):

        for n in range(self.maxNonce):

            if int(block.hash(), 16) <= self.target:

                self.add(block)
                print("Add Block")
                print(block)
                break
            else:
                block.nonce += 1

def editBlock(blockchain,genesisBlock,index):

    i=0
    for x in range(index):
        blockchain.head = blockchain.head.next
        i += 1
    print("==========================")
    print("edit Block no."+str(i))
    print("==========================\n")
    blockchain.head.data = "Edited"

    blockchain.head = genesisBlock
    temp = genesisBlock

    while blockchain.head.next != None:
        if(blockchain.head.hash() != blockchain.head.next.previous_hash):
            print(Fore.LIGHTRED_EX)
            print("Block No. " +  str(blockchain.head.blockNo) + " had been edited...")
            print("=========Show Edited==========")
            print(str(temp))
            print(str(blockchain.head))
            print(str(blockchain.head.next))
            print("=========End Edited=========")
            print(Fore.WHITE)
        temp = blockchain.head
        blockchain.head = blockchain.head.next
