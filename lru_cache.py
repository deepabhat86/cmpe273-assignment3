import functools
import time
cursize = 0

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LRUCache():
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.map = {} 
        self.head = Node(0, 0) # dummy head
        self.tail = Node(0, 0) # dummy tail 
        self.head.next = self.tail 
        self.tail.prev = self.head 
    
    #always add node to head
    def add_node(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove_node(self, node):
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def move_to_head(self, node):
        self.remove_node(node)
        self.add_node(node)

    def pop_tail(self):
        res = self.tail.prev
        self.remove_node(res)
        return res

    def put(self, key, value):
        node = self.map.get(key)
        if not node: 
            new_node = Node(key,value)
            self.map[key] = new_node
            self.add_node(new_node)
            global cursize
            cursize += 1

            if cursize > self.capacity:
                tail = self.pop_tail()
                del self.map[tail.key]
                cursize -= 1
        else:
            node.value = value
            self.move_to_head(node)
        pass
        

    def get(self, key):
        node = self.map.get(key, None)
        if not node:
            return None

        self.move_to_head(node)
        return node.value



def lru_cache(size=5):
    c = LRUCache(size)
    def decorator(func):
        @functools.wraps(func)
        def cache(*args, **kwargs):
            arg_list = []
            if args:
                arg_list.append(', '.join(repr(arg) for arg in args))
            arg_str = ', '.join(arg_list)
            
            cache_key = arg_str
            cache_result = c.get(cache_key)
            
            if cache_result:
                print("cache hit")
                return cache_result

            result = func(*args, **kwargs)
            c.put(cache_key, result)
            return result
        return cache
    return decorator
