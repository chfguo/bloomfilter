# bloomfilter
bloomfilter is a simple Bloom Filter lib for Python, it contains three class:
- BloomFilter: it is in charge of calculating how much bits we need based on the given capacity and error.
  and use Python Bytes as bit array. 
```python
import random
import string
from bloomfilter import BloomFilter

items = []
for i in range(20000):
    random_string = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    items.append(random_string)

bf = BloomFilter(10000,0.05,True)
bitmap = bytes(int(bf.bits/8)+1)

for i in range(10000):
    item = items[i]
    bf.add(bitmap,item)

error = 0
for i in range(10000,20000):
    item = items[i]
    if bf.is_contain(bitmap,item):
        error += 1

print('%s errors in 10000 samples'%error)

    
```
- LocalBloomFilter, a simple wrapper for BloomFilter.
```python
from bloomfilter import LocalBloomFilter
lbf = LocalBloomFilter(1000,0.05)
lbf.add(['apple','banana','C','China','china'])
lbf.is_contain(['apple','Python','Cython','China','china'])
lbf.clean()
```
- RedisBloomFilter, a simple wrapper for BloomFilter uses Redis as backend
```python
from bloomfilter import RedisBloomFilter
from redis import StrictRedis
redis_conn = StrictRedis(host = 'localhost',port = 6379, db = 0)
rbf = RedisBloomFilter(1000,0.05,redis_conn)
rbf.add('bloom','Apple')  # arg 1 is key, arg 2 is item
rbf.is_contain('bloom','Apple')

rbf.add('bloom',['apple','China'])
rbf.is_contain('bloom',['apple','china'])
```
