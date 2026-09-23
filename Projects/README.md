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

```
FUNCTION generate_random_text(markov_model, seed):
	DETERMINE how many start markers were used when the model was built
    SET current_state to the appropriate number of start markers
    INITIALIZE generated_words as an empty list
    SET maximum_words to 200

    WHILE TRUE:
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
- Our team successfully programmed an Nth order Markov Chain algorithm capable of handling any order.
- Successfully created get_next_word function that uses the seed and Markov model provided to choose the next word in the sentence randomly.
- generate_random_text successfully generates random text using the seed and Markov model provided until the end state marker is reached.
- Successfully processed the lines into individual sonnets and stored them in a list in preparation for Markov model generation.
- Our functions passed both tests for the first order and second order operations.

Example successful output:
Seed = 7, Order = 2
When most I wink, then do mine eyes best see, For all the treasure of his spring; For such a counterpart shall fame his wit, Making his style admired every where. Give my love that still, And you in Grecian tires are painted new: Speak of the east, Nor that full star that ushers in the world is grown so bad, Mad slanderers by mad ears believed be. That I have no end: Mine appetite I never saw that you were when first I hallow'd thy fair flower add the rank smell of weeds: But why of two oaths' breach do I find, Happy to have what thou dost review The very part was consecrate to thee: 'Thou single wilt prove none.' 

Seed = 40, Order = 3
Let those who are in favour with their stars Of public honour and proud titles boast, Whilst I, whom fortune of such triumph bars Unlook'd for joy in that I cannot know thy change. In many's looks, the false heart's history Is writ in moods, and frowns, and wrinkles strange. But heaven in thy creation did decree That in thy face sweet love should ever dwell; Whate'er thy thoughts, or thy heart's workings be, Thy looks should nothing thence, but sweetness tell. How like Eve's apple doth thy beauty grow, If thy sweet virtue answer not thy show! 

# Struggles
- Preventing our code from resetting the seed every time the get_next_word function was called required creative solutions. The seed should only be set once other wise the generated text will be repetitive.
- Our Nth order algorithm handles states using tuples. Yet, "the one fish two fish" test we have requires the first order to use only strings for states. This caused the output for first order models to look differently than expected. We elected to use an if else statement to process the first order differently from higher orders.
- Run away code is a genuine concern that we had in this project, and our worries were justified after we created our first few drafts. In short, there is a real possibility that the code gets stuck in a loop between states without reaching an end state. Sometimes it generates too much text before reaching an end state. Other times its infinitely stuck. This problem is bigger in lower order Markov models and less of a concern in higher order model. Our final version of the code mostly eliminated the problem but we invite the peer reviewers to try testing if they can find a seed that causes the code to loop infinitely. Our hard solution to this problem was to create a character limit to how big the generated sentence could be but we removed it in the final version of the code as we have not been able to find a seed that freezes it yet.

# Personal Reflections
## Group Leader
### Ahmed Salman
Markov chains is one of those topics that I learned much about but never tried to implement one myself. This project was a great opportunity to see how far my programming skill can take me. Markov chains really ended up being a wolf in sheep's clothing. A simple idea that becomes much more complicated once you start thinking about generalizations, higher orders, edge cases, efficiency, and more. I am grateful for my teammates as there were many situations where I missed a bug in my code or an edge case that I do not think I would have caught on my own. For example, the seed resetting every time get_next_word is called was something Selin caught. Sonnets did also add the challenge of breaking apart each sonnet and catching the start and end states for each sonnet separately. I really believe that a model like ours is versatile enough to be used for much more than just text and sonnets.

## Other members
### Selin Uenal
This project was much more out of my comfort zone than the previous one. At first, the concept of Markov chains seemed relatively straightforward, but actually building a model and implementing it was much more difficult in practice. We found there were many instances where we could have executed the same thing in fundamentally different ways. We were able to continually discuss as a group to decide on a way before moving forward. We also found there were many edge cases, especially choosing the sonnets as our "poison" since they are multiple texts, with each sonnet having a start and end state, as opposed to one full text, like the other options. Ultimately, I feel like we were able to successfully build a model that we used to generate Shakespearean text. 

### Ildiko Polyak
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
