#!/usr/bin/python

# encoding: utf-8
"""
@author:  郭成锋
@license: (C) Copyright 2014-2018, 济南大象信息技术有限公司
@contact: chf_guo@163.com
@software: 推荐系统
@file: bloomfilter.py.py
@time: 2018/12/13 13:05
@version:
@desc:
@logs:
"""
import traceback
from BloomFilter import BloomFilter

class LocalBloomFilter():

    def __init__(self,capacity,error,prime_length = True):
        self.bf = BloomFilter(capacity,error,prime_length)
        self.bitmap = bytes(int(self.bf.bits/8)+1)

    def add(self,data):
        if isinstance(data,(list,tuple)):
            for v in data:
                assert isinstance(v,str),'add() arg must be a str or list/tuple of strings'
                self.bf.add(self.bitmap, v)
        else:
            assert isinstance(data, str), 'add() arg must be a str or list/tuple of strings'
            self.bf.add(self.bitmap,data)

    def is_contain(self,data):
        if isinstance(data,(list,tuple)):
            for v in data:
                assert isinstance(v,str),'is_contain() arg must be a str or list/tuple of strings'
            return [self.bf.is_contain(self.bitmap, v) for v in data]
        else:
            assert isinstance(data, str), 'is_contain() arg must be a str or list/tuple of strings'
            return self.bf.is_contain(self.bitmap, data)

    def clean(self):
        self.bf.clean_bitmap(self.bitmap)


class RedisBloomFilter():
    def __init__(self, capacity, error, redis_conn, prime_length=True):
        self.bf = BloomFilter(capacity, error, prime_length)
        self.redis_conn = redis_conn

    def add(self, key, data):
        if isinstance(data, (list, tuple)):
            offset = []
            for v in data:
                assert isinstance(v, str), 'add() arg must be a str or list/tuple of strings'
                offset += self.bf.hash(v)
            with self.redis_conn.pipeline() as pipe:
                for o in offset:
                    pipe.setbit(key,o,1)
                pipe.execute()

        else:
            assert isinstance(data, str), 'add() arg must be a str or list/tuple of strings'
            offset = self.bf.hash(data)
            with self.redis_conn.pipeline() as pipe:
                for o in offset:
                    pipe.setbit(key,o,1)
                pipe.execute()


    def is_contain(self, key, data):
        try:
            if isinstance(data, (list, tuple)):
                offset = []
                for v in data:
                    assert isinstance(v, str), 'is_contain() arg must be a str or list/tuple of strings'
                    offset += self.bf.hash(v)

                with self.redis_conn.pipeline() as pipe:
                    for o in offset:
                        pipe.getbit(key, o)
                    result_bits = pipe.execute()
                    result = []
                    for i in range(len(data)):
                        result_bit = result_bits[i*self.bf.hashes:(i+1)*self.bf.hashes]
                        if sum(result_bit) == self.bf.hashes:
                            result.append(True)
                        else:
                            result.append(False)
                    return result

            else:
                assert isinstance(data, str), 'is_contain() arg must be a str or list/tuple of strings'
                offset = self.bf.hash(data)
                with self.redis_conn.pipeline() as pipe:
                    for o in offset:
                        pipe.getbit(key, o)
                    results = pipe.execute()
                    if sum(results) == self.bf.hashes:
                        return True
                    return False
        except Exception:
            print(traceback.format_exc())
            return None

    def clean(self,key):
        self.redis_conn.delete(key)