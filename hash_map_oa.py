# Name: Haris Hambasic
# OSU Email: hambasih@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12 March 2022
# Description: Implementation of a hash table via open addressing


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
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
            if self.table_load() == 0.0:
                return None
            if self.buckets.get_at_index(i) is not None:
                self.buckets.set_at_index(i, None)
                self.size -= 1

        return None

    def get(self, key: str) -> object:
        """
        Returns an element from the hash map

        Args:
            key (string): The key of the element to return

        Return:
            1) None: if the key is not found in the hash map
            2) element (object): if the key is found in the hash map
        """  
        # quadratic probing required
        # Compute initial hash index
        initial_index = self.hash_function(key) % self.buckets.length()
        
        # Check element at initial hash table index
        if self.buckets.get_at_index(initial_index) is not None and self.buckets.get_at_index(initial_index).is_tombstone is not True and self.buckets.get_at_index(initial_index).key == key:
            return self.buckets.get_at_index(initial_index).value
        
        # Compute next index via quadratic probing and continue to probe
        # until you come across the key or you reach an empty bucket
        j = 1
        quadratic_probing_index = (initial_index + (j * j)) % self.buckets.length()
        while self.buckets.get_at_index(quadratic_probing_index) is not None and self.buckets.get_at_index(quadratic_probing_index).is_tombstone is not True and self.buckets.get_at_index(quadratic_probing_index).key != key:
            j += 1
            quadratic_probing_index = (initial_index + (j * j)) % self.buckets.length()
        
        if self.buckets.get_at_index(quadratic_probing_index) is not None and self.buckets.get_at_index(quadratic_probing_index).is_tombstone is False and self.buckets.get_at_index(quadratic_probing_index).key == key:
            return self.buckets.get_at_index(quadratic_probing_index).value
        if self.buckets.get_at_index(quadratic_probing_index) is None:
            return None

    def put(self, key: str, value: object) -> None:
        """
        Inserts an element into the hash map

        Args:
            key (string): The key of the element to insert
            value (object): The value of the elemen to insert

        Return:
            None
        """  
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair

        # Create new key/value pair
        key_value_pair = HashEntry(key, value)

        # RESIZE
        # Check load factor and adjust array if needed
        if self.table_load() >= 0.5:
            if self.capacity * 2 < 1 or self.capacity * 2 > self.buckets.length():
                self.resize_table(self.capacity * 2)

        # Use the hash function to compute an initial index
        initial_index = self.hash_function(key) % self.buckets.length()

        # If the hash table array at the initial index is empty then insert the element and stop
        if self.buckets.get_at_index(initial_index) is None:
            self.buckets.set_at_index(initial_index, key_value_pair)
            self.size += 1

        # 
        elif self.buckets.get_at_index(initial_index).key == key:
            self.buckets.set_at_index(initial_index, key_value_pair)

        # Otherwise, compute the next index via quadratic probing and repeat step above for the new quadratic index
        else:
            j = 1
            quadratic_probing_index = (initial_index + (j * j)) % self.buckets.length()
            while self.buckets.get_at_index(quadratic_probing_index) is not None:
                quadratic_probing_bucket = self.buckets.get_at_index(quadratic_probing_index)
                quadratic_probing_bucket_KEY = quadratic_probing_bucket.key
                if quadratic_probing_bucket_KEY == key:
                    self.buckets.set_at_index(quadratic_probing_index, key_value_pair)
                    return None
                else:
                    j += 1
                    quadratic_probing_index = (initial_index + (j * j)) % self.buckets.length()
            self.buckets.set_at_index(quadratic_probing_index, key_value_pair)
            self.size += 1

        return None

    def remove(self, key: str) -> None:
        """
        Removes an element from the hash map

        Args:
            key (string): The key of the element to remove

        Return:
            None
        """
        # quadratic probing required
        
        # Compute initial hash index
        initial_index = self.hash_function(key) % self.buckets.length()

        # Probe initial element
        if self.buckets.get_at_index(initial_index) is not None:
            if self.buckets.get_at_index(initial_index).is_tombstone == False and self.buckets.get_at_index(initial_index).key == key:
                self.buckets.get_at_index(initial_index).is_tombstone = True
                self.size -= 1
                return None

        # Use quadratic probing scheme to iterate over rest of array
        j = 1
        quadratic_probing_sequence = (initial_index + (j * j)) % self.buckets.length()
        while self.buckets.get_at_index(quadratic_probing_sequence) is not None:
            if self.buckets.get_at_index(quadratic_probing_sequence).is_tombstone == True:
                j += 1
                quadratic_probing_sequence = (initial_index + (j * j)) % self.buckets.length()
                continue
            if self.buckets.get_at_index(quadratic_probing_sequence).key == key:
                self.buckets.get_at_index(quadratic_probing_sequence).is_tombstone = True
                self.size -= 1
                return None
            j += 1
            quadratic_probing_sequence = (initial_index + (j * j)) % self.buckets.length()
        
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
        # quadratic probing required
        
        # Compute initial hash index
        initial_index = self.hash_function(key) % self.buckets.length()
        
        # Check element at initial hash table index
        if (self.buckets.get_at_index(initial_index) is not None and self.buckets.get_at_index(initial_index).is_tombstone is not True) and self.buckets.get_at_index(initial_index).key == key:
            return True
        
        # Compute next index via quadratic probing and continue to probe
        # until you come across the key or you reach an empty bucket
        j = 1
        quadratic_probing_index = (initial_index + (j * j)) % self.buckets.length()
        while (self.buckets.get_at_index(quadratic_probing_index) is not None and self.buckets.get_at_index(quadratic_probing_index).is_tombstone is not True) and self.buckets.get_at_index(quadratic_probing_index).key != key:
            j += 1
            quadratic_probing_index = (initial_index + (j * j)) % self.buckets.length()
        
        if self.buckets.get_at_index(quadratic_probing_index) is None or (self.buckets.get_at_index(quadratic_probing_index) is not None and self.buckets.get_at_index(quadratic_probing_index).is_tombstone is True):
            return False
        return True

    def empty_buckets(self) -> int:
        """
        Counts the number of empty buckets of the hash map

        Args:
            n/a

        Return:
            The number of empty buckets of the hash map
        """  
        number_empty_buckets = 0

        for bucket_index in range(self.buckets.length()):
            if self.buckets.get_at_index(bucket_index) == None or self.buckets.get_at_index(bucket_index).is_tombstone is True:
                number_empty_buckets += 1

        return number_empty_buckets

    def table_load(self) -> float:
        """
        Identifies how "full" the hash table is

        Args:
            n/a

        Return:
            A number indicating the table load of the hash map
        """  
        return self.size / self.buckets.length()

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table once the load factor is greater than or equal to some threshold

        Args:
            new_capacity (int): The new capacity to set for the resized hash table

        Return:
            None
        """  
        # If new_capacity is less than 1 or less than the current number of elements in the map, 
        # the method does nothing.
        if new_capacity < 1 or new_capacity < self.size:
            return None

        # remember to rehash non-deleted entries into new table
        new_hashmap = HashMap(new_capacity, self.hash_function)

        for i in range(self.buckets.length()):
            if self.buckets.get_at_index(i) is None or self.buckets.get_at_index(i).is_tombstone is True:
                continue
            # Get the HashEntry to move into new resized hash table
            key = self.buckets.get_at_index(i).key
            value  = self.buckets.get_at_index(i).value
            new_hash = new_hashmap.hash_function(key) % new_hashmap.buckets.length()
            if new_hashmap.buckets.get_at_index(new_hash) is None:
                new_hashmap.put(key, value)
            elif new_hashmap.buckets.get_at_index(new_hash).is_tombstone is True:
                new_hashmap.put(key, value)

            # Check other indices according to quadratic probing scheme
            else:
                j = 1
                quadratic_probing_index = (new_hash + (j * j)) % new_hashmap.buckets.length()
                while new_hashmap.buckets.get_at_index(quadratic_probing_index) is not None and new_hashmap.buckets.get_at_index(quadratic_probing_index).is_tombstone is False:
                    j += 1
                    quadratic_probing_index = (new_hash + (j * j)) % new_hashmap.buckets.length()
                new_hashmap.put(key, value)

        self.buckets = new_hashmap.buckets
        self.size = new_hashmap.size
        self.capacity = new_hashmap.capacity

        return None

    def get_keys(self) -> DynamicArray:
        """
        Returns all the keys of the hash table

        Args:
            n/a

        Return:
            A dynamic array with all the keys of the hash table
        """  
        keys = DynamicArray()

        for i in range(self.buckets.length()):            
            if self.buckets.get_at_index(i) is not None and self.buckets.get_at_index(i).is_tombstone is False:
                keys.append(self.buckets.get_at_index(i).key)

        return keys


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
    # this test assumes that put() has already been correctly implemented
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

    print("\nCUSTOM - remove example 2")
    print("----------------------")
    m = HashMap(40, hash_function_1)
    m.buckets.set_at_index(0, HashEntry("key115", -880))
    m.buckets.set_at_index(1, HashEntry("key611", -128))
    m.buckets.get_at_index(1).is_tombstone = True
    m.buckets.set_at_index(2, HashEntry("key135", -371))
    m.buckets.get_at_index(2).is_tombstone = True
    m.buckets.set_at_index(3, HashEntry("key108", 700))
    m.buckets.get_at_index(3).is_tombstone = True
    m.buckets.set_at_index(4, HashEntry("key344", 147))
    m.buckets.get_at_index(4).is_tombstone = True
    m.buckets.set_at_index(5, HashEntry("key731", -424))
    m.buckets.get_at_index(5).is_tombstone = True
    m.buckets.set_at_index(6, HashEntry("key507", 131))
    m.buckets.get_at_index(6).is_tombstone = True
    m.buckets.set_at_index(7, HashEntry("key635", 394))
    m.buckets.get_at_index(7).is_tombstone = True
    m.buckets.set_at_index(8, HashEntry("key762", 361))
    m.buckets.get_at_index(8).is_tombstone = True
    m.buckets.set_at_index(9, HashEntry("key408", 1001))
    m.buckets.set_at_index(10, HashEntry("key908", -568))
    m.buckets.get_at_index(10).is_tombstone = True
    m.buckets.set_at_index(11, HashEntry("key378", 320))
    m.buckets.get_at_index(11).is_tombstone = True
    m.buckets.set_at_index(12, HashEntry("key406", -159))
    m.buckets.set_at_index(13, HashEntry("key839", 553))
    m.buckets.get_at_index(13).is_tombstone = True
    m.buckets.set_at_index(16, HashEntry("key982", 620))
    m.buckets.set_at_index(19, HashEntry("key583", -259))
    m.buckets.set_at_index(26, HashEntry("key9", -960))
    m.buckets.set_at_index(33, HashEntry("key17", -458))
    m.buckets.set_at_index(37, HashEntry("key301", 752))
    m.buckets.get_at_index(37).is_tombstone = True
    m.buckets.set_at_index(38, HashEntry("key49", -572))
    m.buckets.get_at_index(38).is_tombstone = True
    m.capacity = 40
    m.size = 7

    m.remove("key408")
    print(m.capacity, m.size)

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
