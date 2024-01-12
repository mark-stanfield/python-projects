
'''
The Item class represents a single item in the game.
'''
class Item:
    
    def __init__(self, name, full_name, weight, capacity, status, description, contents):
        self.name = name  # a one-word name that serves as a unique identifier
        self.full_name = full_name  # includes adjective
        self.weight = weight  # indicates weight or size
        self.capacity = capacity  # a capacity greater than 0 is a container
        self.status = status  # a word that describes the status of this item
        self.description = description  # describs the item when examined
        self.contents = contents  # a list of item names held by this item
    
    def __str__(self):
        result = ''
        count = 0
        for word in self.description.split():
            result += word + ' '
            if count > 65:
                result += '\n'
                count = 0
            else:
                count += len(word) + 1
        return result


'''
The Items class is a collection of all items in the game.
'''
class Items:
    
    def __init__(self, items_file_name):
        
        self.items_dict = {}  # maps an item name to the corresponding Item object
        
        items_file = open(items_file_name, 'r')
        
        name = items_file.readline().strip()
        
        while name != '':
            full_name = items_file.readline().strip()
            weight = int(items_file.readline().strip())
            capacity = int(items_file.readline().strip())
            status = items_file.readline().strip()
            description = items_file.readline().strip()
            if capacity == 0:
                contents = []
            else:
                contents = items_file.readline().split()
                if contents[0] == 'nothing':
                    contents = []
            
            self.items_dict[name] = Item(name, full_name, weight, capacity,
                                         status, description, contents)
            
            items_file.readline()  # consume blank line between item entries
            name = items_file.readline().strip()
    
    
    def __str__(self):
        return str(self.items_dict)
    
    
    def get_item(self, item_name):
        return self.items_dict[item_name]


    def get_total_weight(self, items):
        total = 0
        for item_name in items:
            total += self.items_dict[item_name].weight
        return total
