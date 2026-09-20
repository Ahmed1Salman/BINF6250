#Template from Canvas Module Instructions
#!/usr/bin/env python
from pprint import pprint
import numpy as np
 
def build_markov_model(markov_model, text, order=1):
    pass
 
def get_next_word(current_state, markov_model, seed=42):
    pass
 
def generate_random_text(markov_model, seed=42):
    pass
 
 
if __name__ == "__main__":
    # Pick Your Poison: Sonnets
    poison_markov_model = dict()
    with open("data/sonnets.txt", "r") as poison_text:
        # Process the lines. Consider that sonnets are separated by an empty line.
        # create corpus
        poison_markov_model = build_markov_model(poison_markov_model, corpus, order=2)
 
    print(generate_random_text(poison_markov_model, seed=7))





#Pseudocode
#build_markov_model function
    #Break the text into a list of individual words.
    #Add "order number" of start markers to the front of the list.
    #Add one end marker to back of list.
    #For each word in the padded list:
        #Check whether the current word is already a key in the dictionary. If not, add it as a new key with an empty inner dictionary.
        #Check whether the next word is already recorded under the current word's entry.  If not, add it with a starting count of zero.
        #Add one to the count for current word leads to next word.
    #Once every position has been processed, return the dictionary, showing each current word and next word pair and count.

#get_next_word
    #Look up the current (outter) word as a key in the dictionary, to get the dictionary of possible next (inner) words and each next word is paired with a count of how many times it followed the current word.
    #Add up all the counts for this current word to get a total.
    #For each possible next word, divide its count by the total to get a probability.
    #Using those probabilites as weights, randomly select one next word (using the given seed so results are reproducible).
    #Return the selected next word.


#generate_random_text
    #Set the current word to the start marker, matching however many were used when dictionary was built.
    #Create an empty list to hold the words that will be generated.
    #Repeat until the end marker is generated:
        #Call get_next_word with the current word and the dictionary to pick the next word.
        #Add that word to the list of generated words.
        #Update the current word to be the word that was just picked (sliding the window forward if the order is greater than 1).
    #Once the end marker is generated, stop.
        #Also stop early if a maximum word count is reached as a safeguard in case the end marker never gets generated.
    #Join all the generated words into a single string, seperated by spaces.
    #Return that string.


#Pick Your Poison Script
    #Create an empty dictionary to hold the Markov chain data.
    #Open the sonnets.txt file
    #Read the file in as a list of individual lines.
    #Group these lines together by sonnet, using blank lines as the dividers between one sonnet adn the next.
    #Join the lines within each group back into a single string so that each sonnet becomes one complete string.
    #Store this list of sonnet-strings as the corpus.
    #For each individual sonnet in the corpus:
        #Send this sonnet, along with the existing dictionary and the order, to the function that builds the model
        #Save what that function hands back as the updated dictionary
    #Once every sonnet has been processed, send the finished dictionary to the function that generates random text.
    #Print the text that function returns.