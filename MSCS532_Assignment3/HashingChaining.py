# Hash table implementation using chaining
class HashTable:

    # Create a hash table with a specified size
    def __init__(self, size=10):

        # Number of slots in the table
        self.size = size

        # Create empty chains (lists) for each slot
        self.table = [[] for _ in range(size)]

    # Generate an index for a key
    def hash_function(self, key):

        # Use Python's built-in hash function
        return hash(key) % self.size

    # Insert a key-value pair
    def insert(self, key, value):

        # Find the slot index
        index = self.hash_function(key)

        # Check if key already exists
        for pair in self.table[index]:

            if pair[0] == key:

                # Update existing value
                pair[1] = value
                return

        # Add new key-value pair to the chain
        self.table[index].append([key, value])

    # Search for a key and return its value
    def search(self, key):

        # Find the slot index
        index = self.hash_function(key)

        # Search through the chain
        for k, v in self.table[index]:

            if k == key:
                return v

        # Key not found
        return None

    # Delete a key-value pair
    def delete(self, key):

        # Find the slot index
        index = self.hash_function(key)

        # Search for the key in the chain
        for i, (k, v) in enumerate(self.table[index]):

            if k == key:

                # Remove the key-value pair
                del self.table[index][i]

                return True

        # Key not found
        return False


# Example usage
ht = HashTable()

# Insert records
ht.insert("Amit", 95)
ht.insert("John", 88)
ht.insert("Sarah", 91)

# Search for a record
print("Amit's Score:", ht.search("Amit"))

# Delete a record
ht.delete("John")

# Verify deletion
print("John's Score:", ht.search("John"))