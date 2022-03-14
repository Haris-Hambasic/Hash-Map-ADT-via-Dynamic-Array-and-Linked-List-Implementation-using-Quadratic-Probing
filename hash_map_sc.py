# Name: Haris Hambasic
# OSU Email: hambasih@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12 March 2022
# Description: Implementation of a hash map ADT by using a linked list data structure.


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the hash map so there are no elements in it

        Args:
            n/a

        Return:
            None
        """  
        for i in range(self.buckets.length()):
            self.buckets.get_at_index(i).size = 0
            self.buckets.set_at_index(i, LinkedList())
        
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns an element from the hash map

        Args:
            key (string): The key of the element to return

        Return:
            1) None: if the key is not found in the hash map
            2) element (object): if the key is found in the hash map
        """  
        if self.contains_key(key) is not True:
            return None
        else:
            index = self.hash_function(key) % self.buckets.length()
            
            return self.buckets.get_at_index(index).contains(key).value

    def put(self, key: str, value: object) -> None:
        """
        Inserts an element into the hash map

        Args:
            key (string): The key of the element to insert
            value (object): The value of the elemen to insert

        Return:
            None
        """  
        initial_index= self.hash_function(key) % self.buckets.length()
        linked_list = self.buckets.get_at_index(initial_index)
        
        if linked_list.length() == 0:
            linked_list.insert(key, value)
            self.size += 1
        elif linked_list.contains(key) != None:
            linked_list.remove(key)
            linked_list.insert(key, value)
        else:
            linked_list.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes an element from the hash map

        Args:
            key (string): The key of the element to remove

        Return:
            None
        """
        previous_bucket_node = None
        for i in range(self.buckets.length()):
            current_bucket = self.buckets.get_at_index(i)

            if current_bucket.head is not None:
                current_bucket_node = current_bucket.head
                while current_bucket_node is not None:
                    current_bucket_node_key = current_bucket_node.key
                    if current_bucket_node_key == key:
                        if previous_bucket_node is not None:
                            previous_bucket_node.next = current_bucket_node.next
                        else:
                            current_bucket.head = current_bucket_node.next
                        current_bucket_node = None
                        current_bucket.size -= 1
                        self.size -= 1
                        return None
                    else:
                        previous_bucket_node = current_bucket_node
                        current_bucket_node = current_bucket_node.next

            previous_bucket_node = None
            current_bucket = None
            current_bucket_node = None

        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines if there is an element with the key, in the hash map

        Args:
            key (string): The key of the elment to search for

        Return:
            True: if an element with the key is found in the hash map
            False: if no element with the key is found in the hash map
        """  
        index = self.hash_function(key) % self.buckets.length()

        if self.buckets.get_at_index(index).contains(key):
            return True

        return False

    def empty_buckets(self) -> int:
        """
        Counts the number of empty buckets of the hash map

        Args:
            n/a

        Return:
            The number of empty buckets of the hash map
        """  
        number_of_empty_buckets = 0

        for bucket_index in range(self.capacity):
            if self.buckets.get_at_index(bucket_index).length() == 0:
                number_of_empty_buckets += 1

        return number_of_empty_buckets

    def table_load(self) -> float:
        """
        Identifies how "full" the hash table is

        Args:
            n/a

        Return:
            A number indicating the table load of the hash map
        """  
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table once the load factor is greater than or equal to some threshold

        Args:
            new_capacity (int): The new capacity to set for the resized hash table

        Return:
            None
        """  
        if new_capacity < 1:
            return None

        resized_hash_table = DynamicArray()

        for i in range(new_capacity):
            resized_hash_table.append(LinkedList())

        for i in range(self.buckets.length()):
            current_bucket = self.buckets.get_at_index(i)

            if current_bucket.head is not None:
                list_of_nodes_in_current_bucket = DynamicArray()
                current_bucket = current_bucket.head
                while current_bucket is not None:
                    list_of_nodes_in_current_bucket.append(current_bucket)
                    current_bucket = current_bucket.next
                for i in range(list_of_nodes_in_current_bucket.length()):
                    current_bucket = list_of_nodes_in_current_bucket.get_at_index(i)
                    current_bucket_key = current_bucket.key
                    current_bucket_value = current_bucket.value
                    new_hash = self.hash_function(current_bucket_key) % resized_hash_table.length()
                    resized_hash_table.get_at_index(new_hash).insert(current_bucket_key, current_bucket_value)

        self.buckets = resized_hash_table
        self.capacity = new_capacity

        return None

    def get_keys(self) -> DynamicArray:
        """
        Returns all the keys of the hash table

        Args:
            n/a

        Return:
            A dynamic array with all the keys of the hash table
        """  
        dynamic_array_of_keys = DynamicArray()
        for bucket_index in range(self.buckets.length()):
            bucket = self.buckets.get_at_index(bucket_index)

            element = bucket.head
            while element is not None:
                dynamic_array_of_keys.append(element.key)
                element = element.next

        return dynamic_array_of_keys


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())


    print("\nCUSTOM TEST - remove example 1")
    print("-----------------------")
    m = HashMap(5, hash_function_1)
    for i in range(5):
        m.buckets.set_at_index(i, LinkedList())
    
    m.buckets.get_at_index(0).insert("haris", 26)
    m.buckets.get_at_index(1).insert("sead", 51)
    m.buckets.get_at_index(2).insert("elvedina", 46)
    m.buckets.get_at_index(3).insert("adis", 15)
    m.buckets.get_at_index(4).insert("anis", 20)
    m.buckets.get_at_index(0).insert("oprah", 64)
    m.buckets.get_at_index(0).insert("zen", 99)
    m.remove("haris")
    print(m)