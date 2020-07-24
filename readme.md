> block just like this 
```
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
```
> 有三个重要的数据结构,chain, node, transaction; 安全保证: previous_hash, pow  
> 挖矿主要是pow做一个算力值预测,且sha256不可逆　　
> p2p模式，假设每个主机运行该工程，block_chain最长且符合pow和prevoius_hash等检测的同步block_chain