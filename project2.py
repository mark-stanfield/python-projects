'''
Project 2 - - Scrabble Words - Fall 2023  
Author: Mark Stanfield 906583880

Below is a program which accepts a file containing different
words played in a game of scrabble and return their score, along with
the winner of the game. It keeps track of who's playing (player one or two),
their current word score, and total score. It uses a dictionary, a few
functions, and an abudnance of if statements and for loops to produce
the correct results. Simply, this program accepts a scrabble_words
file and returns the word scores, the player who won, and both
players total scores.

I have neither given or received unauthorized assistance on this assignment.
Signed:  Mark Stanfield
'''

word_score = 0 # define variable
player_one_score = 0 #define variable
player_two_score = 0 #define variable
round = 1 #define variable

points_dictionary = {'A' : 1, 'B' : 3, 'C' : 3, 'D' : 2, 'E' : 1,
               'F' : 4, 'G' : 2, 'H' : 4, 'I' : 1, 'J' : 8,
               'K' : 5, 'L' : 1, 'M' : 3, 'N' : 1, 'O' : 1,
               'P' : 3, 'Q' : 10, 'R' : 1, 'S' : 1, 'T' : 1,
               'U' : 1, 'V' :4, 'W' : 4, 'X' : 8, 'Y' : 4,
               'Z' : 10, '-' : 0}
# define scrabble points
def make_points_dictionary():
    '''
    This function calls and returns
    points_dictionary which is a dictionary
    mapping an uppercase letter to the
    corresponding scrabble score. 
    '''
    return points_dictionary # returns dictionary



def get_word_value(points_dictionary, line):
    '''
    This function accepts the points_dictionary and
    a singular line from the input file. It then sets
    the word score to 0, seperates the line and then
    takes every letter of the scrabble word, finds its
    score, and adds it to the word score. When finished
    with a word it then checks for and bonus information,
    and calculates the additonal points if necessary. It
    finally then adds the word score to the proper player
    and changes the round which keeps track of the player,
    and then returns the word score.
    '''
    global word_score 
    global player_one_score
    global player_two_score
    global round
    word_score = 0
    
    line = line.split() #split list
    for letter in line[0]: # for letter in scrabble word
        letter = letter.upper() # make letter uppercase
        word_score += points_dictionary[letter] # add corresponding dictionary score to player score
    if len(line) != 1: # first see if there is bonus information
        if line[1] == 'DW': 
            word_score += word_score
        elif line[1] == 'TW':
            word_score += word_score * 2
        elif line[1] == 'DL': 
            index_number = line[2] #specifed letter
            current_string = line[0] 
            current_letter = current_string[int(index_number)-1] #index into specified letter
            current_letter = current_letter.upper() #convert to uppercase
            word_score += points_dictionary[current_letter] #add one to word_score
        elif line[1] == 'TL':
            index_number = line[2] #specified letter
            current_string = line[0] 
            current_letter = current_string[int(index_number)-1] #index into specifed letter
            current_letter = current_letter.upper() #convert to uppercase
            word_score += points_dictionary[current_letter] * 2 #add two to word_score
            
            
    if (round % 2) != 0: # determines which player to add score too
        player_one_score += word_score
    elif (round % 2) == 0: # determines which plater to add score too
        player_two_score += word_score
    print(line[0] + ' ' + str(word_score))       #print word + score    
    round += 1 # move to next round
    return word_score     # return score
    
    
       
    
    
    
def print_results(player_one_score, player_two_score):
    '''
    This function accepts the two player scores
    and prints them. Then it compares the two
    to see which one is larger. The larger
    score gets printed, declaring that
    player the winner, or a tie if
    both scores match.
    '''
    print() # for looks 
    print('Player 1 score:', player_one_score) # print player and score
    print('Player 2 score:', player_two_score) # print player and score
    print() # for looks
    if player_one_score > player_two_score: #looks to see whos score is bigger
        print('Player 1 wins!')
    elif player_one_score < player_two_score: # looks to see whos score is bigger
        print('Player 2 wins!')
    elif player_one_score == player_two_score: # checks for tie
        print("I'ts a tie!")

def main():
    '''
    This is the main function of the program. It opens
    an input file that contains the scrabble_words
    and assigns it to a variable. It then uses a for
    loop to call each line in the input file. Each
    line is then put into the get_word_value function
    where the word value is return. When the loop
    concludes, the print_results function is called
    which evalautes the two scores, prints them,
    and prints the winner of the game. 
    '''
    input_file = open('scrabble_words.txt', 'r') #opens input file
    for line in input_file: #calls each line of input file seperate
        get_word_value(points_dictionary, line) #calls get_word_value and passes in point dictionary and line from file
    print_results(player_one_score, player_two_score) #calls print_results function, passes in player scores
    
if __name__ == '__main__':
    main()