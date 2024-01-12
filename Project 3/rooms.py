
'''
The Room class represents a single room in the game.
All distinct areas in the game are considered rooms.
'''
class Room:
    
    def __init__(self, name, description, items_in_room):
        self.name = name
        self.description = description
        self.items_in_room = items_in_room
    
    
    def __str__(self):
        result = self.name + '\n\n'
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
The Rooms class is a collection of all rooms in the game.
'''
class Rooms:
    
    def __init__(self, rooms_file_name):
        
        self.rooms_dict = {}  # maps a room id to its corresponding Room object
        
        rooms_file = open(rooms_file_name, 'r')
        
        room_id = rooms_file.readline().strip()
        
        while room_id != '':
            name = rooms_file.readline().strip()
            description = rooms_file.readline().strip()
            items_in_room = rooms_file.readline().split()
            if items_in_room[0] == 'nothing':
                items_in_room = []
            
            self.rooms_dict[room_id] = Room(name, description,
                                            items_in_room)
            
            rooms_file.readline()  # consume blank line between room entries
            room_id = rooms_file.readline().strip()
    
    
    # Diagnostic purposes only.
    def __str__(self):
        result = ''
        for room_id in self.rooms_dict:
            result += self.rooms_dict[room_id] + '\n'
        return result


    def get_room(self, room_id):
        return self.rooms_dict[room_id]
    
