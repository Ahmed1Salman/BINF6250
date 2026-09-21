# Introduction
This project is centered around the building of a Markov Chain algorithm in Python to simulate the writing of Shakespearean sonnets. This program will read a file with Shakespeare's sonnets and create a dictionary of states and their transition frequencies. The final output will be a randomly generated sentence using the Markov model created.

**Input:** `sonnets.txt`, a text file containing all of Shakespeare’s sonnets, with individual sonnets separated by empty lines.  

**Output:** Randomly generated text based on the patterns learned from the sonnets.

**Objective:** Create a Markov Chain model using the input file then generate random text using that model.

# Pseudocode

1. Create a function `build_markov_model` that accepts a dictionary of dictionaries containing the current Markov model, a string containing the new text and an integer referring to the order of the model and then does the following:  
    - Initializes a dictionary to store the model if the Markov model variable is None.
	- Splits current sonnet into separate words.  
    - Loops through the current sonnet and creates a Markov model based on the order specified.  
    - Note that the starting state for every sonnet will need to be separately counted.  
	- Returns a dictionary of dictionaries containing the states as keys and dictionaries of words and their frequencies as key-value pairs as values.
```
FUNCTION build_markov_model(markov_model, current_sonnet, order):
    IF markov_model is None:
        INITIALIZE markov_model as an empty dictionary

    SPLIT current_sonnet into separate words
    ADD number of starting states based on order
    ADD an ending state

    FOR each position in current_sonnet:
        CREATE the current state based on order
        IDENTIFY the word that follows the current state

        IF the current state is not in markov_model:
            ADD the current state to markov_model

        IF the next word is not stored for the current state:
            ADD the next word with a frequency of 0

        ADD 1 to the next word’s frequency in dictionary

    RETURN markov_model
```

2. Create a function `get_next_word` that accepts a tuple containing the current word, a Markov model, and an integer containing a seed number and then does the following:  
	- Finds the dictionary containing the next possible words and their frequencies from the Markov model.  
	- calculate transition probabilities for all next states using that dictionary.  
	- use the given seed to randomly select the next state.  
```
FUNCTION get_next_word(current_state, markov_model, seed): 
	LOOK UP current_state in markov_model
    GET the inner dictionary of possible next words and their counts
    ADD all the counts together to calculate the total

    FOR each possible next word:
        DIVIDE its count by the total
        STORE the result as its probability

    USE the probabilities as weights and the given seed to randomly
    select one next word

    RETURN the selected next word
```

3. Create a function `generate_random_text` that accepts a Markov model and an integer referring to the random seed used and does the following:  
	- Randomly selects a word from the starting state probabilities in the Markov chain model.  
	- daisy chains words by randomly selecting them based on the previous word until an end state word is selected.  
	- Returns the generated sentence.  
	- Creates a safety cap in case the model never selects an end state. Since words are randomly generated, it is possible that it will keep looping through the Markov model without reaching an end state. The maximum word count prevents the program from continuing indefinitely.

```
FUNCTION generate_random_text(markov_model, seed):
	DETERMINE how many start markers were used when the model was built
    SET current_state to the appropriate number of start markers
    INITIALIZE generated_words as an empty list
    SET maximum_words to 200

    WHILE the number of generated words is less than maximum_words:
        CALL get_next_word using current_state, markov_model, and seed
        STORE the returned word as next_word

        IF next_word is the end marker:
            STOP

        ADD next_word to generated_words
        UPDATE current_state by sliding the window forward and adding next_word

    JOIN generated_words into a single string separated by spaces

    RETURN the generated string
```

4. Read in the sonnets.txt file and process lines
```
INITIALIZE nth_order_markov_model as an empty dictionary
READ sonnets.txt line by line
GROUP the lines into separate sonnets using empty lines
JOIN the lines within each group into one complete sonnet string
SET model order

FOR each sonnet in sonnets.txt:
    CALL build_markov_model
    UPDATE markov_model dict with the returned model

```

5. Print the outputted random generated text:
```
CALL generate_random_text using the completed model and the given seed
PRINT the generated text
```

# Successes
Description of the team's learning points
* 

# Struggles
Description of the stumbling blocks the team experienced
* 

# Personal Reflections
## Group Leader
### Ahmed Salman
Group leader's reflection on the project

## Other members
### Selin Uenal
This project was much more out of my comfort zone than the previous one. At first, the concept of Markov chains seemed relatively straightforward, but actually building a model and implementing it was much more difficult in practice. We found there were many instances where we could have executed the same thing in fundamentally different ways. We were able to continually discuss as a group to decide on a way before moving forward. We also found there were many edge cases, especially choosing the sonnets as our "poison" since they are multiple texts, with each sonnet having a start and end state, as opposed to one full text, like the other options. Ultimately, I feel like we were able to successfully build a model that we used to generate Shakespearean text. 

### Ildiko Polyak
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
