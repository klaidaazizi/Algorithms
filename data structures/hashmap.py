import re
import time


class Node:
    # constructor
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        return f'[Word: {self.key}, Count: {self.value}]'  # returns key and value

class Hashmap:
    def __init__(self):
        self.capacity = 1000  # the size of internal array
        self.buckets = [None] * self.capacity  # the buckets to insert value based on key

    # Generate hash value as index from 0 to capacity of hash table
    def hash(self, key):
        p = 31
        hashvalue = 0
        power = 1
        m = self.capacity

        # polynomial rolling hash function
        for i in range(len(key)):
            hashvalue = (hashvalue + (ord(key[i]) - ord('a') + 1) * power) % m
            power = (power * p) % m

        return hashvalue
    
    # insert new key with value
    def insert(self, key, value):
        # compute hash index for given key
        index = self.hash(key)
        # go to the bucket corresponding to that index
        node = self.buckets[index]
        # if empty spot, add key as new node in the list
        if node is None:
            self.buckets[index] = Node(key, value)
            return
        else:
            new_node = Node(key, value)
            new_node.next = self.buckets[index]
            self.buckets[index] = new_node

    # delete a certain key from list buckets[key]
    def delete(self, key):
        index = self.hash(key)
        node = self.buckets[index]
        # keep track of previous
        prev = None
        # iterate through the list
        while node is not None and node.key != key:
            prev = node
            node = node.next  # found node with given key
        if node is None:
            return None  # key not found
        else:
            value = node.value
            prev.next = prev.next.next  # skip over the node to delete it
            return value

    # increase key
    def increase(self, key):
        # find index in hash table
        index = self.hash(key)
        print(index)
        node = self.buckets[index]
        # traverse list at this index
        while node is not None and node.key != key:
            node = node.next
        # increase node's value by 1
        node.value += 1
        return node.value

    # find key in list of buckets and return its value
    def find(self, key):
        # find index in hash table
        index = self.hash(key)
        node = self.buckets[index]
        # traverse list at this index
        while node is not None and node.key != key:
            node = node.next
        # found node with given key
        if node is None:
            print("Key not found!")
            return
        else:
            return node.value

    def list_all_keys(self):
        keys = []
        for i in range(len(self.buckets)):
            if self.buckets[i] is not None:
                # print(self.buckets[i])
                temp = self.buckets[i]
                while (temp):
                    keys.append(temp)
                    temp = temp.next
        return keys


# create dictionary with key word and value occurrence from a string
def word_dictionary(file):
    text = []
    dictionary = {}

    try:
        with open(file, "r") as f:
            lines = [line.rstrip('\n') for line in f]
        for i in range(len(lines)):
            lines[i] = lines[i].split()
    except IOError:
        print("can't open file")

    for each in lines:
        text.extend(each)
    # print(text)
    for i in range(len(text)):
        text[i] = text[i].lower()
        
        # remove numbers
        text[i] = re.sub(r'\d+', '', text[i])
        
        # remove all punctuation except words and space
        text[i] = re.sub(r'[^\w\s]', '', text[i])
        dictionary[text[i]] = text.count(text[i])
    return dictionary
  
# Main to test (read/write to a file)
def main():
    # hash a string
    hashmap = Hashmap()
    dict = word_dictionary("alice.txt") 
    # script from Alice in Wonderland: https://www.ccs.neu.edu/home/vip/teach/Algorithms/7_hash_RBtree_simpleDS/hw_hash_RBtree/alice_in_wonderland.txt

    for key in dict:
        hashmap.insert(key, dict[key])
    keys = hashmap.list_all_keys()

    # write output into file
    with open("output.txt", "w") as output:
        for each in keys:
            print(each)
            output.write(f'[{each.key}, {each.value}]\n')
    
    # functions testing
    # print("Find 'what': ", hashmap.find("what"))  # should return 32
    # print("Increase by 1: ", hashmap.increase("what")) # should return 33
    # print("Delete 'what': ", hashmap.delete("what")) # should return 33
    # print("Find 'what': ", hashmap.find("what")) # should return "Key Not found" and None

start_time = time.time()
main()
print("\n Algorithm runtime:  %s seconds" % (time.time() - start_time))
