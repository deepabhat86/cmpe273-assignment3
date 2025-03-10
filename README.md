Answer the following question:

* What are the best _k_ hashes and _m_ bits values to store one million _n_ keys (E.g. e52f43cd2c23bb2e6296153748382764) suppose we use the same MD5 hash key from [pickle_hash.py](https://github.com/sithu/cmpe273-spring20/blob/master/midterm/pickle_hash.py#L14) and explain why?

* Ans:
There is another parameter we have to consider which is the false positive probability.  
The size of bit array (m) using following formula , n is the number of items to be stored, p is the false positive probability
(reference: https://en.wikipedia.org/wiki/Bloom_filter#Avoiding_false_positives_in_a_finite_universe)
m = -(n * lg(p)) / (lg(2)^2)

* the number of hash functions can be calculated using following formula where m is the size of the bit array, n is the number of items we would store in filter
k = (m/n) * lg(2) 
(reference: https://en.wikipedia.org/wiki/Bloom_filter#Optimal_number_of_hash_functions)

With a false positive probability of 5 percent:

* Bit Array Size: 6235224

* Hash count: 4

With a false positive probability of 10 percent:

* Bit Array Size: 4792529

* Hash count: 3


# LRU Cache and Bloom Filter

### For bloomfilter ,the output varies with the false positive parameter.
if False positive - 25%

output is
```
(base) MacBook-Pro:cmpe273-assignment3 deepav$ python3 test_bloom_filter.py
'abound' is probably present!
'abounds' is probably present!
'abundance' is probably present!
'bloom' is probably present!
'bolster' is probably present!
'facebook' is a false positive!
'bonny' is probably present!
'abundant' is probably present!
'accessable' is probably present!
'twitter' is definitely not present!
'blossom' is probably present!
'bonus' is probably present!
```

if false positive is - 5%
```
(base) MacBook-Pro:cmpe273-assignment3 deepav$ python3 test_bloom_filter.py
'bolster' is probably present!
'abounds' is probably present!
'abundance' is probably present!
'accessable' is probably present!
'abound' is probably present!
'abundant' is probably present!
'blossom' is probably present!
'facebook' is definitely not present!
'twitter' is definitely not present!
'bonny' is probably present!
'bonus' is probably present!
'bloom' is probably present!
```



### Client response

See the output.txt for the client response on running 4 servers.

The assignment 3 is based on our simple [distributed cache](https://github.com/sithu/cmpe273-spring20/tree/master/midterm) where you have implmented the GET and PUT operations.

## 1. DELETE operation

You will be adding the DELETE operation to delete entires from the distributed cache.

_Request_

```json
{ 
    'operation': 'DELETE',
    'id': 'hash_code_of_the_object',
}
```

_Response_

```json
{
    'success'
}
```

## 2. LRU Cache

In order to reduce unnecessary network calls to the servers, you will be adding LRU cache on client side. On each GET, PUT, and DELETE call, you will be checking against data from a local cache.

Implement LRU cache as Python decorator and you can pass cache size as argument.

```python
@lru_cache(5)
def get():
    ...
    return ...
```

@lru_cache is your implementation as a decorator function and do NOT use any existing LRU libraries.

## 3. Bloom Filter

Finally, you will be implementing a bloom filter so that we can validate any key lookup without hitting the servers. The bloom filter will have two operations:

### Add

This add() function handles adding new key to the membership set.

### Is_member

This is_member() function checks whether a given key is in the membership or not.

On the client side, the GET and DELETE will invoke is_member(key) function first prior to calling the servers while the PUT and DELETE will call add(key) function to update the membership.


```python
@lru_cache(5)
def get(key):
    if bloomfilter.is_member(key):
        return udp_client.get(key)
    else:
        return None
```



