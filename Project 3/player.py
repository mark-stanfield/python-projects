

class Player: #create a class
    
    def __init__(self, player_name): #initalizer
        self.max_capacity = 5 #initalize max_capacity
        self.health = 10 #initalize health
        self.name = player_name #initalize player_name
        self.inventory = set() #initalize and create an empty set representing the players inventory
        
    def max_capacity(self, capacity): #method to define max_capacity
        self.max_capacity = capacity
        
    def take_damage(self, damage): #method to lower player health for eating bread and breaking mirror
        self.health -= damage #lower health by damage taken which integer is passed in
        
        
 
    