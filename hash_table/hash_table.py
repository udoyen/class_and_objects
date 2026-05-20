class HashTable:
    def __init__(self):
        self.collection = {}

    def hash(self, string_para):
        return sum(map(ord, string_para))

    # def add(self, key, value):
    #     hash_value = self.hash(key)
    #     if hash_value not in self.collection:
    #         self.collection[hash_value] = {key: value}
    #     else:
    #         self.collection[hash_value][key] = value

    def add(self, key, value):
        self.collection.setdefault(self.hash(key), {})[key] = value
    
    def remove(self, key):
        key_hash = self.hash(key)
        if key_hash in self.collection:
            self.collection[key_hash].pop(key, None)

    def lookup(self, key):
        return self.collection.get(self.hash(key), {}).get(key, None)