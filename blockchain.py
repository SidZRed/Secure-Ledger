import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []  
        
        #Initial block
        self.new_block(previous_hash=1, proof=100)

    # Create and add a new block to the blockchain
    def new_block(self, proof, previous_hash=None):
        block = {
            'index':len(self.chain) + 1,
            'timestamp':time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1]) 
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    # Add a new transaction to the list of transactions
    def new_transaction(self, sender, reciever, amount):
        self.current_transactions.append({
            'sender':sender,
            'reciever':reciever,
            'amount':amount
        })

        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        '''
        Proof of work algorithm:
        - The proof of work is a number p' such that the hash(pp') contains 4 leading zeros
        - p is the previous proof, and p' is the new proof
        '''
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof

    @staticmethod
    def valid_prrof(last_proof, proof):
        '''
        Validates the proof using the proof of work algorithm
        '''
        check = f'{last_proof}{proof}'.encode()
        check_hash = hashlib.sha256(check).hexdigest()
        return check_hash[:4] == "0000"
    
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '') # Generate a random uuid for the node

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Reward for finding the proof
    blockchain.new_transaction(
        sender="0",
        reciever=node_identifier,
        amount=1
    )
    
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message':'New block forged',
        'index':block['index'],
        'transactions':block['transactions'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction added to block {index}'}    
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


