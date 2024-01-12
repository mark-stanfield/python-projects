'''
Project 3 - Text Adventure - Fall 2023  
Author: John Lewis - lewis63

Modified by:  <Mark Stanfield 905683880>

The program presents a text-based adventure game with
multiple rooms and items.
'''

from game import Game

def main():

    game = Game()
    
    finished = False
    
    while not finished:
        print()
        command_input = input('> ')
        print()
        command = game.clean_command(command_input)
        if command == 'quit':
            finished = True
        else:
            game.process_command(command)    


# Call main like this to keep Web-CAT happy:
if __name__ == '__main__':
    main()
