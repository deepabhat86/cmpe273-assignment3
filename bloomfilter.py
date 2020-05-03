import hashlib
import math
from bitarray import bitarray 
from pickle_hash import hash_code_hex

class BloomFilter(object): 
    def __init__(self, items_count,false_prob): 
        self.false_prob = false_prob 
        self.size = self.get_size(items_count,false_prob) 
        self.hash_count = self.get_hash_count(self.size,items_count) 
        self.bit_array = bitarray(self.size) 
        self.bit_array.setall(0) 
  
    def add(self, item): 
        previousHashes=[]
        previousHashes.append(item)
        for i in range(self.hash_count):
            new_hash=hash_code_hex(previousHashes[i].encode('utf-8'))
            digest = int(new_hash,16) % self.size 
            previousHashes.append(str(new_hash))
            self.bit_array[digest] = True
  
    def is_member(self, item): 
        previousHashes=[]
        previousHashes.append(str(item))
        for i in range(self.hash_count): 
            new_hash=hash_code_hex(previousHashes[i].encode('utf-8'))
            digest = int(new_hash,16) % self.size
            # if any of bit is False then,its not present 
            if self.bit_array[digest] == False:   
                return False
            previousHashes.append(str(new_hash))
        return True
  
    def get_size(self,n,p): 
        ''' 
        Return the size of bit array(m) to used using 
        following formula , n is the number of items to be stored, p is the false positive probability
        (reference: https://en.wikipedia.org/wiki/Bloom_filter#Avoiding_false_positives_in_a_finite_universe)
        m = -(n * lg(p)) / (lg(2)^2) 
        '''
        m = -(n * math.log(p))/(math.log(2)**2) 
        return int(m) 
  
    def get_hash_count(self, m, n): 
        ''' 
        Return the hash function(k) to be used using 
        following formula where m is the size of the bit array, n is the number of items we would store in filter
        k = (m/n) * lg(2) 
        https://en.wikipedia.org/wiki/Bloom_filter#Optimal_number_of_hash_functions
        '''
        k = (m/n) * math.log(2) 
        return int(k) 
        
if __name__ == "__main__":
    bloomfilter=BloomFilter(10,.05)
    bloomfilter.add("hello")
    print(bloomfilter.is_member("hello"))