import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        raw_hash = hashlib.sha256(block_string.encode())
        hex_hash = raw_hash.hexdigest()
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        block_string = json.dumps(block_string, sort_keys=True)
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # return guess_hash[:3] == '000'
        return guess_hash[:6] == '000000'


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/last_block', methods=['GET'])
def last_block():
    return jsonify(blockchain.last_block), 200


@app.route('/mine', methods=['POST'])
def mine():
    r = request.get_json()
    try: data = r.json()
    except ValueError: return jsonify({'message': 'you sent non-json'}), 400

    if 'proof' not in data or 'id' not in data:
        return jsonify({'message': 'missing req info'}), 400
    else: 
        proof, miner_id = int(data['proof']), data['id']

    if blockchain.valid_proof(blockchain.last_block, proof):
        prev_hash = blockchain.hash(blockchain.last_block)
        blockchain.new_block(proof, prev_hash)
        return jsonify({'message': 'new block forged'}), 200
    
    return jsonify({'message': 'proof rejected'}), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain, 
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

