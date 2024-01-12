'''
Project 3 - Text Adventure - Fall 2023  
Author: John Lewis - lewis63

Modified by:  <Mark Stanfield 905683880>

This is the main Game class of the text adventure.
It's responsible for cleaning the commands input by
the user and then processing them.
'''

from rooms import Rooms
from routes import Routes
from items import Items
from player import Player #NEWSTUFF
import random

class Game:
    
    def __init__(self):

        self.rooms = Rooms('rooms_data.txt')
        self.routes = Routes('routes_data.txt')
        self.items = Items('items_data.txt')
                
        self.current_room = 'library'
        
        # The directions set includes all recognized directions.
        self.directions = {'north', 'south', 'east', 'west',
            'northeast', 'northwest', 'southeast', 'southwest',
            'up', 'down'}
        
        # The aliases dictionary maps an abbreviation to its proper word.
        self.aliases = {'n' : 'north', 's' : 'south', 'e' : 'east', 'w' : 'west',
            'ne' : 'northeast', 'nw' : 'northwest', 'se' : 'southeast', 'sw' : 'southwest',
            'u' : 'up', 'd' : 'down', 'l' : 'look', 'ex' : 'examine', 'i' : 'inventory',
            't' : 'take', 'get' : 'take', 'stairs' : 'staircase', 'coin': 'doubloon',
            'photo' : 'photograph', 'picture' : 'photograph', 'pic' : 'photograph'}
        
        # The curios set includes all items that must be put into the cabinet.
        self.curios = {'candlestick', 'doll', 'doubloon', 'necklace',
                       'photograph', 'ring', 'unicorn'}
        
        # The containers set includes all items that can store other items.
        self.containers = {'cabinet', 'chest', 'clock'}
        
        # The verbs set includes all recognized verbs.
        self.verbs = {'climb', 'close', 'dig', 'drop', 'examine', 'go',
            'inventory', 'lock', 'look', 'open', 'put', 'quit', 'read',
            'swim', 'take', 'touch', 'type', 'unlock', 'break', 'eat'} #NEWSTUFF
        
        # The inventory set is the set of all items the player is carrying.
       
         
        # Start the game!
        self.print_welcome()
        self.print_room(self.current_room)

    
    def clean_command(self, command_input):
        ''' This method transforms the command as input by the user
        into a standard form that can be processed. '''
        
        command = ''
        
        # Remove adjectives by replacing the item full name with its name.
        # For example, changes 'curio cabinet' to 'cabinet'.
        for item_name in self.items.items_dict:
            item = self.items.get_item(item_name)
            if item.full_name in command_input:
                command_input = command_input.replace(item.full_name, item.name)
        
        words = command_input.split()
        
        if len(words) == 0:
            return ''
        
        # Remove articles. For example, changes 'climb the ladder'
        # to 'climb ladder'.
        for word in words:
            if word in {'the', 'a', 'an'}:
                words.remove(word)
       
        # Replace any alias word with the standard word.
        # For example, replace 'n' with 'north'.
        for i in range(len(words)):
            if words[i] in self.aliases:
                words[i] = self.aliases[words[i]]

        # If the first word is a direction, add 'go' verb.
        # For example, change 'north' to 'go north'.
        if words[0] in self.directions:
            words.insert(0, 'go')
        
        # Replace 'look at' with 'examine'
        if len(words) >= 2 and words[0] == 'look' and words[1] == 'at':
            words[0] = 'examine'
            words.pop(1)
        
        # If the first word is a recognized verb, construct the
        # standard command. Otherwise, the command is 'invalid'.
        if words[0] in self.verbs:
            for word in words:
                command += word + ' '
        else:
            command = 'invalid'
                
        # Remove the trailing space.
        command = command.strip()
        
        return command


    def process_command(self, command):
        ''' Process the cleaned-up standardized command. Separate
        methods are defined for each verb. '''
        
        words = command.split()
        
        # the quit command is processed in main
        
        if len(words) == 0:
            responses = ['Speak up!', 'I beg your pardon?',
                "What's that you say?", 
                "Your lack of elocution is embarassing."]
            print(random.choice(responses))
            return
        
        verb = words[0]
        
        if self.player.health < 10: #NEWSTUFF
            self.player.health += 1 #NEWSTUFF
        
        if verb == 'go':
            self.process_go(words)
        elif verb == 'take':
            self.process_take(words)
        elif verb == 'drop':
            self.process_drop(words)
        elif verb == 'inventory':
            self.process_inventory()
        elif verb == 'look':
            self.print_room(self.current_room)
        elif verb == 'examine':
            self.process_examine(words)
        elif verb == 'open':
            self.process_open(words)
        elif verb == 'close':
            self.process_close(words)
        elif verb == 'lock':
            print("You don't need to lock anything.")
        elif verb == 'unlock':
            self.process_unlock(words)
        elif verb == 'put':
            self.process_put(words)
        elif verb == 'touch':
            self.process_touch(words)
        elif verb == 'climb':
            self.process_climb(words)
        elif verb == 'swim':
            self.process_swim()
        elif verb == 'read':
            self.process_read(words)
        elif verb == 'type':
            self.process_type(words)
        elif verb =='eat':
            self.process_eat(words) #NEWSTUFF
        elif verb == 'break':
            self.process_break(words) #NEWSTUFF
        elif verb == 'dig':
            self.process_dig()
        else:
            print("I don't know how to do that.")
    
    
    # Command methods ================================
    
    def process_go(self, words):
        # Get the routes out of the current room
        if self.current_room in self.routes.routes_dict:
            routes = self.routes.get_routes(self.current_room)
        else:
            routes = {}  # when there are no normal directions out
        
        if len(words) == 1:
            print('You have to tell me which way to go.')
        elif words[1] not in self.directions:
            print("I don't know that direction.")
        elif words[1] in routes:
            self.current_room = routes[words[1]]
            self.print_room(self.current_room)
        elif self.current_room == 'beach4' and words[1] == 'north':
            print('The rocks prevent you from simply walking north.')
        elif self.current_room == 'cove' and words[1] == 'south':
            print('The rocks prevent you from simply walking south.')
        elif self.current_room in {'beach1', 'beach2', 'beach3', 'beach4'} and words[1] == 'east':
            print('The ocean is too rough for swimming today.')
        elif self.current_room == 'clearing' and words[1] == 'south':
            print('The shed door is locked. Try the keypad.')
        elif self.current_room in {'cornfield1', 'cornfield2', 'cornfield3', 'cornfield4', 'cornfield5'}:
            # loop to same room if in the cornfield maze and it's not a valid path:
            self.print_room(self.current_room)            
        else:
            print("You can't go that way from here.")
    
    
    def process_inventory(self):
        if len(self.player.inventory) == 0: #NEWSTUFF
            print("You're not carrying anything.")
        else:
            print('You are currently carrying:')
            for item_name in self.player.inventory: #NEWSTUFF
                item = self.items.get_item(item_name)
                print('   ' + item.full_name)


    def process_take(self, words):
        if len(words) == 1:
            print('You have to tell me what you want to take.')
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        elif words[1] in self.player.inventory: #NEWSTUFF
            print("You're already carrying that.")
        else:
            item = self.items.get_item(words[1])
            room = self.rooms.get_room(self.current_room)
            if item.name in room.items_in_room:
                if item.weight >= 10:
                    print("You can't carry that.")
                elif self.items.get_total_weight(self.player.inventory) + item.weight > int(self.player.max_capacity): #NEWSTUFF
                    print("You can't carry it with your current load.")
                else:
                    self.player.inventory.add(item.name) #NEWSTUFF
                    room.items_in_room.remove(item.name)
                    print('Taken.')
            else: # check if item is in an open container in the room
                for item_name_in_room in room.items_in_room:
                    if item_name_in_room in self.containers:
                        container = self.items.get_item(item_name_in_room)
                        if item.name in container.contents and container.status == 'open':
                            if self.items.get_total_weight(self.player.inventory) + item.weight > int(self.player.max_capacity): #NEWSTUFF
                                print("You can't carry it with your current load.")
                            else:
                                self.player.inventory.add(item.name) #NEWSTUFF
                                container.contents.remove(item.name)
                                print('Taken.')
                            break
                else:  # not found in any container in room
                    print("I don't see that here.")


    def process_drop(self, words):
        if len(words) == 1:
            print('You have to tell me what you want to drop.')
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        elif words[1] not in self.player.inventory: #NEWSTUFF
            print("You're not carrying that.")
        else:
            room = self.rooms.get_room(self.current_room)
            room.items_in_room.append(words[1])
            self.player.inventory.remove(words[1]) #NEWSTUFF
            print('You dropped the ' + words[1] + '.')


    def process_examine(self, words):
        if len(words) == 1:
            print('You have to tell me what you want to examine.')
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        else:
            item = self.items.get_item(words[1])
            room = self.rooms.get_room(self.current_room)
            if item.name not in room.items_in_room and item.name not in self.player.inventory: #NEWSTUFF
                print("I don't see that here.")
            else:
                print(item)
                if item.capacity > 0 and item.status == 'open':
                    self.print_container_contents(item)

                painting = self.items.get_item('painting')
                if item.name == 'painting':
                    print('While examining the painting your hand brushes against it...\n')
                    self.print_ghost_visit(painting.status)
                    painting.status = 'touched'
                    cabinet = self.items.get_item('cabinet')
                    cabinet.status = 'open'

                necklace = self.items.get_item('necklace')
                if item.name == 'scarecrow' and necklace.status == 'unfound':
                    necklace.status = 'found'
                    room.items_in_room.append('necklace')
                    print('As you inspect the scarecrow a necklace falls from its stuffing.')
                    

    def process_open(self, words):
        room = self.rooms.get_room(self.current_room)
        if len(words) == 1:
            print('You have to tell me what you want to open.')
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        elif words[1] not in room.items_in_room and words[1] not in self.player.inventory: #NEWSTUFF
            print("I don't see that here.")
        elif words[1] not in self.containers:
            print("You can't open that.")
        else:
            item = self.items.get_item(words[1])
            if item.name == 'chest' and item.status == 'buried':
                print("The chest is mostly buried in the sand. You can't open it.")
            elif item.status == 'locked':
                print("It's locked.")
            elif item.status == 'open':
                print("It's already open.")
            else: # status is 'closed'
                item.status = 'open'
                print("You opened the " + item.full_name + '.')
                if item.name in self.containers:
                    self.print_container_contents(item)

    
    def process_close(self, words):
        room = self.rooms.get_room(self.current_room)
        if len(words) == 1:
            print('You have to tell me what you want to close.')
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        elif words[1] not in room.items_in_room and words[1] not in self.player.inventory: #NEWSTUFF
            print("I don't see that here.")
        elif words[1] not in self.containers:
            print("You can't close that.")
        else:
            item = self.items.get_item(words[1])
            if item.name == 'chest' and item.status == 'buried':
                print("The chest is already closed, and mostly buried in the sand.")
            elif item.status == 'locked':
                print("It's already closed. In fact, it's locked up tight.")
            elif item.status == 'closed':
                print("It's already closed.")
            else: # status is 'open'
                item.status = 'closed'
                print("You closed the " + item.full_name + '.')

    
    def process_unlock(self, words):
        room = self.rooms.get_room(self.current_room)
        if len(words) == 1:
            print('You have to tell me what you want to unlock.')
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        elif words[1] not in room.items_in_room and words[1] not in self.player.inventory: #NEWSTUFF
            print("I don't see that here.")
        elif words[1] not in self.containers:
            print("You can't unlock that.")
        elif words[1] == 'cabinet':
            print("There's no lock on the cabinet, but you can't get it open. Weird.")
        else:
            item = self.items.get_item(words[1])
            if item.status == 'open':
                print("It's not locked. In fact, it's open.")
            elif item.status == 'closed':
                print("It's already unlocked, but it's still closed.")
            else:  # must be the locked chest
                if item.status == 'buried':
                    print("The chest is mostly buried in the sand. You can't reach the lock.")
                elif 'key' not in self.player.inventory: #NEWSTUFF
                    print("You don't have the key to the chest.")
                else:
                    item.status = 'closed'
                    print("You unlocked the chest using the skeleton key.")
    
   
    def process_put(self, words):
        room = self.rooms.get_room(self.current_room)
        if len(words) < 4:
            print('Use the format "put item in container".')
        elif words[1] not in self.items.items_dict:
            print("I don't know what " + words[1] + ' is.')
        elif words[1] not in self.player.inventory: #NEWSTUFF
            print("You're not holding a " + words[1] + '.')
        elif words[3] not in self.items.items_dict:
            print("I don't know what " + words[3] + ' is.')
        elif words[3] not in room.items_in_room and words[3] not in self.player.inventory: #NEWSTUFF
            print("I don't see the " + words[3] + ' here.')
        else:
            item = self.items.get_item(words[1])
            container = self.items.get_item(words[3])
            if container.name not in self.containers:
                print("You can't put anything in a " + container.name + '.')
            elif container.status != 'open':
                print('The ' + container.name + ' is not open.')
            elif self.items.get_total_weight(container.contents) + item.weight > container.capacity:
                print("It won't fit.")
            else:
                container.contents.append(item.name)
                self.player.inventory.remove(item.name) #NEWSTUFF
                print("You put the " + item.name + ' in the ' + container.name + '.')
                if container.name == 'cabinet':
                    if item.name in self.curios:
                        print('You hear a ghostly whisper, "Yes..."')
                        if set(container.contents) == self.curios:
                            self.print_winner()  # You did it!
                    else:
                        print('You hear a ghostly moan of anguish, "No, no..."')
                if container.name == 'clock' and item.name == 'wrench':
                    print('\nThe wrench serves as a replacement pendulum and starts swinging')
                    print('back and forth! The clock chimes loudly one time and then the')
                    print('whole clock slides to side, revealing a set of stairs going up.')
                    room.items_in_room.append('staircase')
                    self.routes.routes_dict['library']['up'] = 'attic'
                    room.description += ' A staircase leads up.'
            
    
    def process_touch(self, words):
        room = self.rooms.get_room(self.current_room)
        if len(words) == 1:
            print('You have to tell me what you want to touch.')
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        elif words[1] not in room.items_in_room and words[1] not in self.player.inventory: #NEWSTUFF
            print("I don't see that here.")
        elif words[1] == 'painting':
            painting = self.items.get_item('painting')
            self.print_ghost_visit(painting.status)
            painting.status = 'touched'
            cabinet = self.items.get_item('cabinet')
            cabinet.status = 'open'
        elif words[1] == 'scarecrow':
            necklace = self.items.get_item('necklace')
            if necklace.status == 'unfound':
                necklace.status = 'found'
                room.items_in_room.append('necklace')
                print('When you touch the scarecrow a necklace falls from its stuffing.')
        else:
            responses = ['Okay...', 'If you say so...',
                         'Hey, whatever floats your boat.']
            print(random.choice(responses))


    def process_climb(self, words):
        room = self.rooms.get_room(self.current_room)
        if len(words) == 1:
            print('You have to tell me what you want to climb.')
        elif words[1] in {'up', 'down'}:
            self.process_go(['go', words[1]])
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        elif words[1] not in room.items_in_room:
            print("I don't see that here.")
        elif self.current_room == 'beach4' and words[1] == 'rocks':
            print("It's dangerous, but you scramble over the rocks...\n")
            self.current_room = 'cove'
            self.print_room(self.current_room)
        elif self.current_room == 'cove' and words[1] == 'rocks':
            print("You climb back over the rocks...\n")
            self.current_room = 'beach4'
            self.print_room(self.current_room)
        elif self.current_room == 'garage' and words[1] == 'ladder':
            print("You climb up the ladder...\n")
            self.current_room = 'loft'
            self.print_room(self.current_room)
        elif self.current_room == 'loft' and words[1] == 'ladder':
            print("You climb down the ladder...\n")
            self.current_room = 'garage'
            self.print_room(self.current_room)
        elif self.current_room == 'library' and words[1] == 'staircase':
            print("You climb the stairs...\n")
            self.current_room = 'attic'
            self.print_room(self.current_room)
        elif self.current_room == 'attic' and words[1] == 'staircase':
            print("You descend the stairs...\n")
            self.current_room = 'library'
            self.print_room(self.current_room)
        else:
            print("You can't climb that.")


    def process_swim(self):
        room = self.rooms.get_room(self.current_room)
        if self.current_room in {'beach1', 'beach2', 'beach3', 'beach4'}:
            print("The waves are too rough today to go swimming.")
        elif self.player.health < 10: #NEWSTUFF
            print("You are to tired to swim.") #NEWSTUFF
        elif self.current_room == 'pond':
            print("You swim to the island...\n")
            self.current_room = 'island'
            self.print_room(self.current_room)
        elif self.current_room == 'island':
            print("You swim back the way you came...\n")
            self.current_room = 'pond'
            self.print_room(self.current_room)
        else:
            print("You can't swim here!")


    def process_read(self, words):
        room = self.rooms.get_room(self.current_room)
        if len(words) == 1:
            print('You have to tell me what you want to read.')
        elif words[1] not in self.items.items_dict:
            print("I don't know what that is.")
        elif words[1] not in self.player.inventory and words[1] not in room.items_in_room: #NEWSTUFF
            print("I don't see that here.")
        elif words[1] == 'book':
            if 'book' not in self.player.inventory: #NEWSTUFF
                print("You're not holding the book.")
            else:
                self.print_book()
        elif words[1] == 'brick' and self.current_room == 'patio':
            print('Someone has scratched some kind of formula into the brick:')
            print('math.ceil(math.sin(45) * 10 ** 4)')
        else:
            print("You can't read that!")


    def process_type(self, words):
        room = self.rooms.get_room(self.current_room)
        if self.current_room != 'clearing':
            print("There's nothing to type on!")
        elif len(words) == 1:
            print('You have to tell me what you want to type.')
        elif words[1] != '8510': # typing on the shed keypad
            print("The keypad emits a rude sound effect of rejection.")
        else:
            print("The keypad beeps happily and the shed door slides into the wall")
            print("with a surprising high-tech 'swooosh'.")
            self.routes.routes_dict['clearing']['south'] = 'shed'
            room.items_in_room.remove('keypad')
            room.description = room.description.replace('with a keypad on the door',
                                                        'with an open doorway')
            

    def process_dig(self):
        if self.current_room not in {'beach1', 'beach2', 'beach3', 'beach4', 'cove', 'dune'}:
            print("You can't dig here.")
        elif 'spoon' not in self.player.inventory: 
            print("You lack an appropriate digging tool.")
        elif self.player.health < 10: #NEWSTUFF
            print("You lack the strength to dig.") #NEWSTUFF
        else:
            chest = self.items.get_item('chest')  # half-buried in cove
            ring = self.items.get_item('ring')  # buried in beach 3
            if self.current_room == 'cove' and chest.status == 'buried':
                chest.status = 'locked'
                chest.full_name = 'sturdy chest'  # changed from 'half-buried chest'
                chest.description = 'The chest looks like something out of a pirate movie.'
                print('You dig with the serving spoon and uncover the chest.')
            elif self.current_room == 'beach3' and ring.status == 'buried':
                ring.status = 'chill'
                room = self.rooms.get_room(self.current_room)
                room.items_in_room.append('ring')
                print('You dig with the serving spoon and uncover a ring!')
            elif self.current_room == 'dune':
                print('You dig with the serving spoon, but the sand just shifts back.')
            else:
                print('You dig with the large serving spoon...')
                responses = ['Wheeee! Playing in the sand is fun!',
                    'You build a stunning sandcastle, but the waves wash it away.',
                    'You dug yourself a hole! But then the waves fill it back in.']
                print(random.choice(responses))
               
               
               
    def process_eat(self, words): #NEWSTUFF, create and define function
        if len(words) == 1: #NEWSTUFF, checks to make sure command is more than just 'eat'
            print('You have to tell me what you want to eat.') #NEWSTUFF
        elif words[1] not in self.items.items_dict: #NEWSTUFF, checks to make sure item passed in exists in the game
            print("I don't know what that is.") #NEWSTUFF
        elif words[1] not in self.player.inventory: #NEWSTUFF, checks to make sure player has the item in their inventory
            print('You have nothing to eat.') #NEWSTUFF
        elif words[1] == 'bread': #NEWSTUFF, check to make sure that the item in the inventory is in fact bread
            print('You eat the moldy bread, your health lowers by 5') #NEWSTUFF
            self.player.take_damage(5) #NEWSTUFF, calls player method to lower health from eating the bread
            self.player.inventory.remove('bread') #NEWSTUFF, removes bread from player inventory
        
        
            
            
    def process_break(self, words): #NEWSTUFF, creates function
        if len(words) == 1: #NEWSTUFF, checks to make sure command is more than just 'break'
            print('You have to tell me what you want to break.') #NEWSTUFF
        elif words[1] not in self.items.items_dict: #NEWSTUFF, checks to make sure item passed in exists in the game
            print("I don't know what that is.") #NEWSTUFF
        elif words[1] != 'mirror': #NEWSTUFF, checks to make sure item passed in is called mirror
            print('You cannot break that') #NEWSTUFF
        elif self.current_room != 'bedroom': #NEWSTUFF, checks to make sure player is in the bedrood (with the mirror)
            print('There is no mirror to break.') #NEWSTUFF
        elif 'spoon' not in self.player.inventory: #NEWSTUFF, checks to see if player has a neccesary tool
            if 'wrench' not in self.player.inventory: #NEWSTUFF, checks to see if player has a neccesary tool
                print("You don't have the tools to break.") #NEWSTUFF
        else: #NEWSTUFF, if all conditions are met allow process
            mirror = self.items.get_item('mirror') #NEWSTUFF
            if mirror.status == 'broken': #NEWSTUFF, checks to see if mirror is already broken
                print('The mirror is already broken.') #NEWSTUFF
            else: #NEWSTUFF, if not broken allow breaking to occur
                print('You break the mirror, but it hurts you. Your health lowers by 5.') #NEWSTUFF
                mirror.status = 'broken' #NEWSTUFF, change mirror status
                mirror.full_name = 'broken mirror' #NEWSTUFF, change mirror full_name
                mirror.description = 'The mirror is shattered.' #NEWSTUFF, change mirror description
        
        
            
    # Utility methods ================================
    

    def print_welcome(self):
        print('Welcome to Snarfblat!\n')
        print('This really needs a better name!\n')
        player_name = input('What is your name? \n> ') #NEWSTUFF
        self.player = Player(player_name) #NEWSTUFF
        print('You awake as if from a dream to find yourself in a...\n')


    def print_room(self, room_id):
        room = self.rooms.get_room(room_id)
        print(room)
        if len(room.items_in_room) > 0:
            print()
            for item_name in room.items_in_room:
                item = self.items.get_item(item_name)
                print('There is a ' + item.full_name + ' here.')
                if item.name in self.containers and item.status == 'open':
                    self.print_container_contents(item)


    def print_container_contents(self, container):
        if len(container.contents) == 0:
            print('The ' + container.name + ' is empty.')
        else:
            print('The ' + container.name + ' contains:')
            for item_name in container.contents:
                item = self.items.get_item(item_name)
                print('   ' + item.full_name)


    def print_ghost_visit(self, painting_status):
        print('The moment you touch the painting you begin to hear an anguished moaning.')
        print('The air starts to shimmer! An apparition appears before you!')
        print("It's the old woman from the painting! She's not a happy camper.")
        print('"Help me!" she moans. "Retrieve my treasures! Set things right!"')
        print('The ghostly image fades...')
        if painting_status == 'untouched':
            print('\nYou hear a click as the cabinet unlocks and opens.')


    def print_winner(self):
        print("\nThe ghost of the old woman appears to you again! She's clearly in a")
        print("much better mood.\n")
        print('"You did it! Thank you for retrieving my precious things!" she says.')
        print("\"You've made me so happy! If only I could reward your diligence and")
        print("bravery. Wait, I know, I'll grant you your heart's desire...\"\n")
        print('She closes her eyes, concentrating, but after a few moments opens')
        print('them again.\n')
        print('"Nope, it\'s no good. Not even my magical ghostly powers can ensure')
        print('that you\'ll get an A in Dr. Lewis\' class. He\'s a right git.\n')
        print('"But thanks anyway," she says, pounding her fist on her chest.')
        print('"Peace out!"\n')
        print('The ghost then vanishes, leaving you to wonder if it was all worth it...')


    def print_book(self):
        print("You peruse the book. It's riveting. Here's the gist:\n")
        print("You can move around using commands like 'go north' or just 'north'.")
        print("You can take and drop items, such as 'take book'.")
        print("You can see what you're carrying using 'inventory'.")
        print("You can remind yourself where you are using 'look'.")
        print("You can end the adventure using 'quit'.\n")
        print("Several words can be abbreviated, such as 'n' for 'north' or")
        print("'i' for inventory.\n")
        print('Here are some other things to try if the situation calls for it:\n')
        print('examine book')
        print('climb ladder')
        print('put ring in cabinet')
        print('read sign')
        print('dig')
        print('touch wrench')
        print('swim')
        print('type 1010\n')
        print('Now carry on, bold adventurer!')
    