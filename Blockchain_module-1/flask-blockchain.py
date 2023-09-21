from flask import Flask, jsonify
from blockchain import Blockchain


# Creating a web app
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()


# Mining a Blockchain
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': "Congrats! You just mined a block.",
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


# Get the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Check the validity
@app.route('/is_valid', methods=['GET'])
def is_valid():
    validity = blockchain.is_chain_valid(blockchain.chain)
    if validity:
        response = {'message': "All good. The Blockchain is valid."}
    else:
        response = {'message': "Houston, we have a problem with this Blockchain."}
    return jsonify(response), 200


# Run the app
app.run(host='0.0.0.0', port=5000)
