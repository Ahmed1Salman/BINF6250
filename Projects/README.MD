# Introduction
This project is centered around the building of a Markov Chain algorithm in Python to simulate the writing of Shakespearean sonnets. This program will read in a .txt file with Shakespeare's sonnets and create a dictionary of states and probabilities of each states emissions. The final output will be a randomly generated sentence using the Markov model created.

# Pseudocode
Put pseudocode in this box:

```
input: sonnets.txt
output: Randomly generated text using the sonnets as a model

Objective: Create a Markov Chain model using the sonnets.exe file then generate random text using that model

Pseudocode:
1- read in the sonnets.txt file
2- create a function called build_markov_model that accept a dictionary of dictionaries containing the current Markov model, a str containing the new text and an integer referring to the order of the model and then does the following:
	a. splits the text into separate sonnets and then separate words.
	b. initialize dictionary to store states in.
	c. loops through the current sonnet and creates a Markov model based on the order specified.
	d. Note that the starting state for every sonnet will need to be separately counted.
	d. Returns a dictionary of dictionaries containing the states as keys and dictionaries of words and their frequencies as key-value pairs as values.
3- create a function called get_next_word that accepts a tuple containing the current word, a Markov model, and an integer containing a seed number and then does the following:
	a. Finds the dictionary containing the next possible words and their frequencies from the Markov model.
	b. calculate transition probabilities for all next states using that dictionary.
	c. use the given seed to randomly select the next state.
4- create a function called generate_random_text that accepts a Markov model and an integer referring to the random seed used and does the following:
	a. randomly selects a word from the starting state probabilities in the Markov chain model.
	b. daisy chains words by randomly selecting them based on the previous word until the desired sentence length is achieved.
	c. Returns the generated sentence.
```

# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
