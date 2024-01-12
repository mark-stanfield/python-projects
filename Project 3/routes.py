
'''
The Routes class represents all routes currently available
in the game using the 'go' command.
'''
class Routes:
    
    def __init__(self, routes_file_name):
        
        self.routes_dict = {}
        
        # The routes_dict maps a room id (the current location) to a
        # dictionary of routes. Each route maps a direction to a room.
        #
        # For example, the following entry represents the fact that
        # you can move from the Library east to the Foyer or west
        # to the Patio:
        #
        # { 'library' : { 'east' : 'foyer', 'west' : 'patio' }
        
        routes_file = open(routes_file_name, 'r')
        
        for line in routes_file:
            room_id, direction, destination = line.split()
            if room_id in self.routes_dict:
                self.routes_dict[room_id][direction] = destination
            else:
                self.routes_dict[room_id] = {direction : destination}
            
            
    def __str__(self):
        result = ''
        for room_id in self.routes_dict:
            result += room_id + ': ' + str(self.routes_dict[room_id]) + '\n'
        return result


    def get_routes(self, from_room):
        return self.routes_dict[from_room]


