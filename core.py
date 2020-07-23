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

    self.new_blcok(previous_hash = 1, proof = 100)

  def new_blcok(self):
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

