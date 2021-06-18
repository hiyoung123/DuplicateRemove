#!usr/bin/env python
#-*- coding:utf-8 -*-

from src.simhash import SimHash


class DuplicateRemove:

    def __init__(self, hash_size, block_num):
        self.hash_size = hash_size
        self.block_num = block_num
        self.block_size = hash_size/block_num
        self.index = [{} for _ in range(self.block_num)]
        self.doc_hash_dict = {}
        self.hash = SimHash(hash_size)

    def insert(self, doc, doc_id):
        encoded = self.encode(doc)
        for b in range(self.block_num):
            key = ''
            for i in range(0, len(encoded), self.block_num):
                key += encoded[i]
            if key not in self.index[b]:
                self.index[b][key] = []
            self.index[b][key].append(doc_id)
        self.doc_hash_dict[doc_id] = encoded

    def contains(self, doc):
        docs = self.recall(doc)
        doc_hash_code = self.encode(doc)
        for doc_id in docs:
            other_hash_code = self.get_hash_code(doc_id)
            if self.similar(other_hash_code, doc_hash_code):
                return True
        return False

    def recall(self, doc):
        result = []
        encoded = self.encode(doc)
        for b in range(self.block_num):
            key = ''
            for i in range(0, len(encoded), self.block_num):
                key += encoded[i]
            doc_ids = self.index[b].get(key, [])
            result.extend(doc_ids)
        return result

    def similar(self, hash_code1, hash_code2):
        t1 = self.covert_str_to_int(hash_code1)
        t2 = self.covert_str_to_int(hash_code2)
        distance = self.hamming(t1, t2)
        return True if distance <= self.block_num-1 else False

    def encode(self, text):
        return self.hash.encode(text)

    def hamming(self, doc1, doc2):
        return self.hash.hamming(doc1, doc2, self.hash_size)

    def get_hash_code(self, doc_id):
        return self.doc_hash_dict.get(doc_id, None)

    def covert_str_to_int(self, text):
        return self.hash.covert_str_to_int(text)


if __name__ == '__main__':

    with open('../data/document1', 'r', encoding='utf-8') as f:
        text1 = f.read()
    with open('../data/document2', 'r', encoding='utf-8') as f:
        text2 = f.read()
    with open('../data/document3', 'r', encoding='utf-8') as f:
        text3 = f.read()

    dr = DuplicateRemove(64, 4)
    if not dr.contains(text1):
        dr.insert(text1, 1)
    print(dr.contains(text1))
    print(dr.contains(text2))
    print(dr.contains(text3))
