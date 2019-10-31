#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: ZhaoTongxu

"""
区块链：一种分类账技术，使用区块链进行交易的比特币以及其他加密货币的交易记录会被按时间顺序存储，并且是公开存储。

通俗的说，它是一个公共数据库，其中新数据存储在称为块的容器中，并被添加到具有过去添加的数据的不可变链(因此是块链).
在比特币和其他加密货币的情况下，这些数据是一组交易记录，当然，数据可以是任何类型的。

本位使用50行的Python代码制作了一个简单的blockchain。
"""

import hashlib as hasher
import datetime as date


"""
下面是一个定义的块。
在块链中，每个块都有时间戳和可选的索引，这里同时存储两者，并且为了帮助确保整个块链的完整性，每个块将具有自识别散列。
像比特币一样，每个块的散列将是块的索引，时间戳，数据以及前一个块的哈希散列的加密散列。
"""
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        # 创建一个块的加密散列
        sha = hasher.sha256()
        sha.update(str.encode(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)))

        return sha.hexdigest()


"""
上面是一个块结构，在创建一个块链时，需要向实际的链条添加块。
因为每个块都需要上一个块的信息，这里就有一个问题：块区中的第一个块如何产生。
因此，第一个块，或起源块，是一个特殊的块。在许多情况下，它是手动添加的或具有运行添加的唯一逻辑值。
"""


"""
定义一个可以创建起源块的函数。
该块的索引为0， 它在"previous hash"参数中具有任意数据值和任意值
"""
def create_genesis_block():
    # Manually construct a block with index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), 'Genesis Block', '0')


"""
定义一个用来生成块链中后续块的函数。
该函数以块链中的前一个块作为参数，创建要生成的块的数据，并返回具有其相应数据的新块。
当新块得到先前块中的哈希信息时，块链的完整性随着每个新的块而增加。
如果我们没有这样做，外界信息会更容易"改变过去"，并用自己的更新变化来代替我们的链条。
这个哈希链作为加密证明，有助于确保一旦块被添加到块链中，它不能被替换或删除。
"""
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash

    return Block(this_index, this_timestamp, this_data, this_hash)


"""
在这个例子中，blockchain本身就是一个简单的Python列表。列表的第一个元素是起源块。
在列表后面添加块。
"""
# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blocks should we add to the chain after the genesis block
num_of_blocks_to_add = 20

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    # Tell everyone about it!
    print('Block #{} has been added to the blockchain!'.format(block_to_add.index))
    print('Hash: {}\n'.format(block_to_add.hash))

