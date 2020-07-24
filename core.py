import hashlib
import json

from time import time
from urllib.parse import urlprase
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

class BlockChain:
  def __init__(self):
    self.current_transactions = []
    self.chain = []
    #无序不重复集合
    self.nodes = set()

    self.new_blcok(previous_hash = 1, proof = 100)

  def register_node(self, address):
    #域名路径解析 scheme = 'http', netloc ='192.168.1.102',path = '/path', query='ct=1&op=2'
    parsed_url = urlprase(address)
    if parsed_url.netloc:
      self.nodes.add(parsed_url.netloc)
    elif parsed_url.path
      self.nodes.add(parsed_url.path)
    else:
      raise ValueError('Invalid url')

  def valid_chain(self, chain):
    last_block = chain[0]
    current_index = 1
    
    while current_index < len(chain):
      block = chain[current_index]
      print(f'{last_blcok}')
      print(f'{block}')
      print('\n_________\n')
      
      #hash check
      last_block_hash = self.hash(last_block)
      if block['previous_hash'] != last_block_hash
        return False
      
      #POW　check
      if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash)
        return False

      last_block = block
      current_index += 1

    return True
  
  def resolve_conflicts(self):
    neighbours = self.nodes
    new_chain = None

    max_length = len(self.chain)

    for node in neighbours:
      response = requests.get(f'http://{node}/chain')

      if response.status_code == 200:
        length = response.json()['length']
        chain = response.json()['chain']

        if length > max_length and self.valid_chain(chain):
          max_length = length
          new_chain = chain

    if new_chain:
      self.chain = new_chain
      return True

    return False
    

  def new_block(self):
    #creat a new block and add it into the chains
    block = {
      'index': len(self.chain) + 1,
      'timestamp': time(),
      'transaction': self.current_transactions,
      'proof': proof,
      'previous_hash': previous_hash or self.hash(self.chain(-1)),
    }

    //这个地方重置
    self.current_transactions = []
    self.chain.append(block)
    return block

  def new_transaction(self, sender, recipient, amount):
    #add a new transaction into a tranctionLists
    """
    sender : address of the sender
    这也是一种注释方式
    """
    self.current_transactions.append({'sender': sender, 'recipent': recipient, 'amount': amount})
    return self.last_blcok['index'] + 1


  #静态方法，不用去实例化
  @staticmethod
  def hash(block):
    #hash a block
    blcok_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(blcok_string).hexdigest()


  #可以当作类的属性使用
  @property
  def last_blcok(slef):
    #return the last block in the chain
    return self.chain[-1]

  def proof_of_work(slef, last_blcok):
    last_proof = last_blcok['proof']
    last_hash = self.hash(last_blcok)

    proof = 0
    while self.valid_proof(last_proof, proof, last_hash) is False:
      proof += 1
    
    return proof

  @staticmethod
  def valid_proof(last_proof, proof, last_hash):
    guess = f'{last_proof}{proof}{last_hash}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess.hash[:4] === "0000"


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = BlockChain()

#挖矿
@app.route('/mine', methods=['GET'])
def mine():
  last_block = blockchain.last_blcok
  proof = blockchain.proof_of_work(last_block)

  #奖励1比特币
  blockchain.new_transaction(
    sender="0",
    recipient=node_identifier,
    amount=1,
  )

  previous_hash = blockchain.hash(last_block)
  block = blockchain.new_block(proof, previous_hash)

  response = {
    'message': "New Block Forged",
    'index': block['inde'],
    'transactions': block['transactions'],
    'proof': block['proof'],
    'previous_hash': block['previous_hash'],
  }
  return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
  values = request.get_json()

  required = ['sender', 'recipient', 'amount']
  if not all(k in values for k in required):
    return 'Missing values', 400
  
  index = blockchain.new_transaction(values['sender'], values['recipent'], values['amount'])

  response = {'message': f'Transaction will be added to Block {index}'}
  return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def chain:
  response = {
    'chain': blockchain.chain,
    'length': len(blockchain.chain),
  }
  return jsonify(response), 200

@app.route('/node/register', methods=['POST'])
def register_nodes():
  values = request.get_json()

  nodes = values.get('nodes')
  if nodes is None:
    return "Error : supply a valid list of nodes", 400

  for node in nodes:
    blockchain.register_node(node)

  response = {
    'message': 'new nodes have been added',
    'total_nodes': list(blockchain.nodes),
  }
  return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
  replaced = blockchain.resolve_conflicts()

  if replaced:
    response = {
      'message': 'our chain was replaced',
      'new_chain': blockchain.chain,
    }
  else:
    response = {
      'message': 'our chain is authorization',
      'new_chain': blockchain.chain
    }

  return jsonify(response), 200


if __name__ = '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
  args = parser.parse_args()
  port = args.port

  app.run(host='0.0.0.0', port=port)