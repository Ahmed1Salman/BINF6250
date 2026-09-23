# Introduction
This project centers on building a Markov Chain algorithm in Python to simulate the writing of Shakespearean sonnets. The program takes sonnets.txt, a text file containing all of Shakespeare's sonnets with individual sonnets separated by blank lines, and constructs a dictionary of states and their transition frequencies, learning which words tend to follow which others throughout the text. Using that model, the program generates new, randomly produced text by walking through the learned transition probabilities from a starting state until an end state is reached, with the ultimate goal of a Markov Chain model generalized to work at any order.

Beyond the technical objective, this project also asked us to practice a genuinely asynchronous collaborative workflow, with three group members working across different schedules and, at times, different points in the same day, coordinating through GitHub and Teams rather than in person. That collaborative dimension turned out to be just as significant a part of the project as the Markov Chain logic itself, and is reflected throughout this README.


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
Our team successfully built an Nth-order Markov Chain algorithm capable of handling any order, rather than a version hardcoded for a single specific order. We tested this across several orders directly against expected output, confirming that both first-order and second-order models correctly matched the "one fish two fish" example from the assignment, and that higher orders, including an order as high as 150, produced sensible, well-formed output drawn directly from the sonnets. The `get_next_word` function correctly uses the given seed and Markov model to select a next word weighted by real transition probabilities, and `generate_random_text` correctly daisy-chains these selections together until an end-state marker is reached, producing a complete, readable passage rather than stopping prematurely or looping indefinitely. We also successfully processed the raw sonnets file into individual sonnets, using blank lines to separate them, and fed each one into the model separately so that sonnet boundaries are respected rather than treated as one continuous, undifferentiated text.

Two representative examples of successful output demonstrate the model working well at different orders. At seed 7 with order 2, the model generated a passage beginning "When most I wink, then do mine eyes best see, For all the treasure of his spring..." and continuing through several coherent Shakespearean-style clauses before correctly terminating. At seed 40 with order 3, the model generated a different, longer passage beginning "Let those who are in favour with their stars Of public honour and proud titles boast..." Both outputs read as recognizably Shakespearean in vocabulary and rhythm, while still being newly generated rather than reproductions of a single sonnet verbatim, which is the intended behavior of the model.

One success worth naming is that all three of us, working somewhat independently at different points, arrived at three separate working implementations of the same three functions, and comparing them directly turned out to be one of the most valuable parts of the whole project. Each implementation made different, defensible choices. One consistently represented every state as a tuple regardless of order; another branched explicitly, using a plain string at order one and a tuple only at higher orders; a third built parallel lists for word probabilities rather than a dictionary. Placing all three side by side and tracing through each one's logic as a group gave us a clearer picture of the tradeoffs involved than any one of us would have reached working alone.

That same pattern of learning from each other showed up in how our overall workflow organically developed, beyond just the code itself. One person tended to lay the foundation for a given section, a second would elevate it, and a third would polish it further, so that everyone contributed at a different stage and was able to catch mistakes the others had missed. Despite being such an asynchronous project, the workflow really shone, turning what could have been a purely logistical challenge into a genuine, ongoing source of learning from one another.


# Struggles
The most significant technical struggle we encountered was a bug in how the random seed was being handled inside `generate_random_text`. Our first instinct, understandably, was to pass the seed into `get_next_word` on every single call inside the generation loop. This seemed reasonable, but it meant the random number generator was being reset to the exact same starting point every time, which caused the generated text to become stuck repeating the same short cycle of words indefinitely, since the "random" choice at a given state was the same deterministic choice every time. This bug was independently discovered twice, by two different people working in two different implementations, before we understood exactly what was happening and why. The correct fix, which we ultimately adopted, is to set the seed only once, at the very beginning of `generate_random_text`, and then pass no seed at all into subsequent calls to `get_next_word`, allowing numpy's internal random state to continue advancing naturally between calls rather than resetting each time.

There was a second, less visible side to this same bug. One of us initially fixed the repetition by passing a different, changing seed value into each call inside the loop, based on how many words had been generated so far. This did successfully stop the repetitive output, but it introduced a subtler problem that was not obvious because that fix ignored the function's seed parameter entirely inside the loop. Calling `generate_random_text` with two different seed values would silently produce identical output both times, meaning the seed parameter had stopped controlling reproducibility at all. This was only discovered by comparing that implementation directly against a teammate's more complete version. It was a useful lesson that a fix can resolve the specific symptom you noticed while quietly introducing a different, less visible problem, and that passing your own tests is not the same as having fully solved the underlying issue.

A second real design challenge came from reconciling how our Nth-order model represents a state internally. A model that represents a state as a tuple of the previous order words works cleanly for any order greater than one, but the assignment's own first-order test case, "one fish two fish," expects a plain single word as a state rather than a one-element tuple. This meant a generalized, always-tuple implementation produced technically correct but differently shaped output at order one than what the test case expected. We ultimately resolved this by branching on whether the order is exactly one, storing the state as a plain string in that case and as a tuple only when the order is greater than one, and handling both cases explicitly wherever a state gets used or advanced. This was a case where more than one internally consistent approach was defensible, and required group discussion rather than there being one obvious answer from the start.

We also spent real time worried about the possibility of runaway generation, meaning a case where the model becomes stuck cycling between a small number of states and never reaches an end marker, or takes an extremely long time to do so. This concern turned out to be justified in our earliest drafts, particularly at low orders, where a small number of possible transitions at a given state made it entirely plausible to cycle for a long stretch before randomly landing on the end marker. Our first solution to this was a hard cap on the generated sentence's length, as a safety backstop in case an end state was never reached. In our final version, however, after testing extensively across a range of seeds and orders without finding a case that failed to terminate or looped for an excessive length, we made the decision to remove this cap rather than leave it in as a possibly unnecessary safeguard. We want to be transparent that we did not exhaustively prove no such seed exists, and we invite anyone reviewing this project to try to find a seed that causes the generation to loop for an unreasonable length or fail to terminate.

Finally, working asynchronously as a group of three, across different schedules and different time zones, introduced real coordination challenges beyond the code itself. On separate occasions, a fix made by one teammate had not yet been seen or incorporated by another before further changes were made independently, which briefly resulted in two of us fixing the same underlying seed bug separately, in two separate files, before realizing what had happened. At one point, checking the shared repository very early in the morning, before another teammate's already-pushed file had been noticed, led to a round of review being conducted on an incomplete picture of the current state of the code, which then had to be redone once the missing file was found. None of these moments reflect a breakdown in communication so much as the genuine difficulty of coordinating asynchronous work under a tight deadline, and each one gave us a clearer sense of how to structure both our workflow and our use of GitHub going forward.


# Personal Reflections
## Group Leader
### Ahmed Salman
Markov chains is one of those topics that I learned much about but never tried to implement one myself. This project was a great opportunity to see how far my programming skill can take me. Markov chains really ended up being a wolf in sheep's clothing. A simple idea that becomes much more complicated once you start thinking about generalizations, higher orders, edge cases, efficiency, and more. I am grateful for my teammates as there were many situations where I missed a bug in my code or an edge case that I do not think I would have caught on my own. For example, the seed resetting every time get_next_word is called was something Selin caught. Sonnets did also add the challenge of breaking apart each sonnet and catching the start and end states for each sonnet separately. I really believe that a model like ours is versatile enough to be used for much more than just text and sonnets.

## Other members
### Selin Uenal
This project was much more out of my comfort zone than the previous one. At first, the concept of Markov chains seemed relatively straightforward, but actually building a model and implementing it was much more difficult in practice. We found there were many instances where we could have executed the same thing in fundamentally different ways. We were able to continually discuss as a group to decide on a way before moving forward. We also found there were many edge cases, especially choosing the sonnets as our "poison" since they are multiple texts, with each sonnet having a start and end state, as opposed to one full text, like the other options. Ultimately, I feel like we were able to successfully build a model that we used to generate Shakespearean text. 

### Ildiko Polyak
Coming into this project, I carried forward the same approach that worked well for me last week, writing thorough, plain-English pseudocode before touching any real code, and working through each function slowly, one step at a time, until I fully understood why each line was needed rather than just what it did. I spent a lot of time foundationally understanding Markov Chain models before tackling any element of the project because this concept was new to me and it took me a while to comprehend how to approach working through the project. I found that trying to rush any part of this project, whether the pseudocode, the actual coding, or the Git workflow, reliably led to mistakes and confusion rather than saving time. I had to re-establish that pace with myself and with my own working process, since it is easy to let a long, tiring session push you toward rushing right when careful attention matters most.

My group this week worked much more asynchronously than my group last week. This led to more opportunities to learn from my group by seeing how they improved existing code, rather than us trying to create code together in real time. There was also a noticeable difference in the importance of properly utilizing GitHub this time, which I believe better reflects real-world working conditions for anyone in bioinformatics.


# Generative AI Appendix
Generative AI was not used for this project.
