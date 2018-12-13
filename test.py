#!/usr/bin/python

from bloomfilter import BloomFilter,RedisBloomFilter,LocalBloomFilter

from redis import StrictRedis

import random
import string

items = []
for i in range(20000):
    random_string = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    items.append(random_string)

for i in range(20000):
    if random.randint(1,10)>5:
        items.append(items[i])


bf = BloomFilter(10000,0.05,True)

bitmap = bytes(int(bf.bits/8)+1)

setmap = set()

for i in range(10000):
    item = items[i]
    bf.add(bitmap,item)
    setmap.add(item)

error = 0
num = len(items)
for i in range(10000):
    index = random.randint(0,num-1)
    item = items[index]
    if (item in setmap) != (bf.is_contain(bitmap,item)):
        error += 1

print('%s errors in 10000 samples'%error)


bitmap2 = bytes(int(bf.bits/8)+1)
for i in range(10000):
    item = items[i]
    bf.add(bitmap2,item)

error = 0
for i in range(10000,20000):
    item = items[i]
    if bf.is_contain(bitmap2,item):
        error += 1

print('%s errors in 10000 samples'%error)










lbf = LocalBloomFilter(1000,0.05)
lbf.add(['apple','banana','C','China','china'])
lbf.is_contain(['apple','Python','Cython','China','china'])


redis_conn = StrictRedis(host = '192.168.2.38',port = 6379, db = 0)

rbf = RedisBloomFilter(1000,0.05,redis_conn)
rbf.add('bloom','Apple')
rbf.is_contain('bloom','Apple')

rbf.add('bloom',['apple','China'])
rbf.is_contain('bloom',['apple','China'])





