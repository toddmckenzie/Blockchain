import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

DIFFICULTY = 5

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block

        self.new_block(previous_hash='===============', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []
        self.chain.append(block)

        return block

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        hash = hashlib.sha256(block_string).hexdigest()

        return hash

    @property

    def last_block(self):
        return self.chain[-1]

    def valid_proof(self, block_string, proof):
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:DIFFICULTY] == "0" * DIFFICULTY

# Instantiate our Node

app = Flask(__name__)

# Generate a globally unique address for this node

node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain

blockchain = Blockchain()

@app.route('/mine', methods=['POST']) #was get now post
#NEW PROOF SENT BY CLIENT.

def mine():
    try:
        values = request.get_json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        return "Error" 

    required = ['proof', 'id']
    if not all(k in values for k in required):
        response = {'message': "Missing Values"}
        return jsonify(response), 400
    
    submitted_proof = values['proof']

    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True)
    if blockchain.valid_proof(last_block_string, submitted_proof):
        previous_hash = blockchain.hash(blockchain.last_block)
        new_block = blockchain.new_block(submitted_proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'block': 'block'
            }

        return jsonify(response), 200
    else:
        response = {
            'message': "Proof invalid or already submitted"
        }
        return jsonify(response), 200

@app.route('/chain', methods=['GET'])

def full_chain():

    response = {

        'length': len(blockchain.chain),

        'chain': blockchain.chain

    }

    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])

def last_block():

    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200

# Run the program on port 5000

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=4004)