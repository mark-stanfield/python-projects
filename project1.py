'''
Project 1 - Game Score Evaluator - Fall 2023
Author: Mark Stanfield VT pid

This program evalutes the score of a game and returns the preformance level based on the score.

I have neither given or received unauthorized assistance on this assignment.
Signed: Mark Stanfield
'''


def determine_level(score):
    '''Evalutes 'score' and returns the preformance level based on the
parameters of the score'''
    if score >= 0 and score <= 100:
        return 'Beginner'
    # determines if score is between 0 and 100, inclusive, if true returns 'Beginner'
    elif score >= 101 and score <= 500:
        return 'Intermediate'
    # determines if the score is between 101 and 500, inclusive, if true return 'Intermediate'
    elif score >= 501 and score <= 1000:
        return 'Advanced'
    # determines if the score is between 501 and 1000, inclusive, if true returns 'Advanced'
    elif score > 1000:
        return 'Expert'
    # determines if the score is greater than 1000, exclusive, if true returns 'Expert'

def evaluate_score(score):
    '''determines if the score value passed as an arguement is greater than 0,
    deciding if the function should evaluate the score or not'''
    if (score) < 0:
        print('Error invalid input. Score must be greater than 0.')
        #evaluates score to see if it is a negative integer
    else:
        print('The preformance level is', determine_level(score), '.') 
        #prints performance level then calls the determine_level function which returns the score level
       
def main():
    '''main function, displays welcome and thank you messages,
    calls function evaluate score to determine performance level of game score,
    unless the value 'q' is entered'''
    print('Welcome to the game score evalutator!') #prints welcome message
    print() #creates extra space, for looks
    score = input('''Enter a game score (or 'q' to quit): ''')
    while score != 'q': #sets up condition with a exiting sentinal value
        score = int(score) #convert to interger
        evaluate_score(score) #calls evaluate_score function
        print() #creates extra space, for looks
        score = input('''Enter a game score (or 'q' to quit): ''') #statement asking for score input
    print() #creates extra space, for looks
    print('Thanks for using the game score evaluator!') #thank you message displayed after breaking while loop
    
if __name__ == '__main__': #calling the main function to make Web-CAT happy
    main()