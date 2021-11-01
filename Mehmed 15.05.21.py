#!/usr/bin/env python
# coding: utf-8

# # CODE BREAKING WITH STATISTICAL PHYSICS

# By Zhuoshang Han, Mark Ko, Mehmed Ozbas and Erin Pollard

# In this Project, we will be exploring different methods we can use to decypher codes which involves using code and human intervention at certain points. Code breaking is a powerful tool that can be used for many purposes including national security and privacy. Nowadays we have blockchain-based cryptocurrencies that rely on cryptography for safety and fidelity measures. The methods we use throughout this project are different to the ones used in the 20th century by mathematicians and computer scientists.  These methods include: 
# - Using a program to find out the cyclic shift (using trial and error, and some work by hand), 
# - Using character frequencies from a long text to find patterns and comparing these patterns to the coded messages which includes coding spaces and punctuation, 
# - Using frequency of bigrams (pairs of consecutive characters) to establish patterns in text that is found in the coded messages 
# - Exploring Markov and Metropolis methods to decypher coded messages
# 
# Once we have coded these methods, we can apply it to the coded messages and decode them.

# In[2]:


#We created a text file coded_message which holds all the messages to be decoded
#We are calling message1 to 12 from a coded_message.py
from coded_message import*


# ##  Section 1: Solving simple cyclic shifts
# In the first message, we are told that the cipher is simply a cyclic shift of the 27 characters. E.g.  shift of 2 would map A → C, B → D, . . . , Y → space, Z → A, space → B. We therefore tackled the first message using a trial and error method, as the encryption used a simple Caesar cipher (shift) [1]. This involved trying the different possible shifts of the 27 characters and checking by hand whether any of the shifts produced readable texts in English. We found that by shifting each character 9 places to the left (I.e. J to A) allowed us to translate the message back. The decoded message is outputted below.

# In[3]:


number = 9 
shift   = int(number) # This is the number of characters we are shifting to the left in order to decode

coded_message_1 = list(message1) # Here we call the 1st message from our external file and store each character
                                 # of the string in a separate element in a list
    
# This list contains all viable characters (only upper case letters and the space character)
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',chr(32)]

# For each coded character in the coded message, we find its index in the alphabet (27th if its the white space)
# We then shift the index 9 places to the right. If the original index + 9 would be greater than 26 then we have 
# adjusted for this by using the modulo operator %. This ensures all new indexes range from 0 to 26 only.
# We then take the coded character and replace it with a new character which corresponds to the new index. Then we print
# the new character.
for letter in coded_message_1: 
    oldindex = alphabet.index(letter)
    newindex = (oldindex + shift) % len(alphabet)
    newletter = alphabet[newindex]
    print(newletter, end="")


# ## Section 2: Using a long text to help analyse patterns
# The other messages each use an arbitrary permutation of the characters, so trying all the possibilities was no longer practical. 
# Instead we used the statistical properties of the text. We found Moby Dick as this was a large body of text and downloaded it to analyse.
# We replaced all lower case letters with upper case, and removed all extra characters (i.e. $). 

# Run the cell below once to create a file to store the Moby Dick text into a .txt file alongside this notebook, this avoids us repeatedly spamming someone's server.

# In[4]:


import requests
link = "https://www.gutenberg.org/files/2701/2701-0.txt"
moby = requests.get(link).text
with open('moby.txt','w',errors='ignore') as f:
    f.write(moby.upper()) # write to file


# The re.sub function replaces any occurrences of any substrings [2]. The [ ] creates a list of characters and the ^ negates this list so that these characters are not replaced. The ' ' argument indicates what you want to replace the chosen charatcers with. In moby_exception we replace everything that isn't alphabetical or a hyphen or apostrophe with a white space. The second use of the re.sub function uses '', indicating we want the re.sub function to replace all the hyphens and apostrophes with nothing, effectively deleting them.

# In[5]:


import re

# This code opens our pre-made text file and reads it into a string variable called moby
with open('moby.txt','r',errors='ignore',encoding = 'utf-8') as f:
    moby=f.read() 
    
# Here we deal with non alphabetical characters and those that aren't white spaces.
moby_exception = re.sub(r'[^A-Z\-\'"]+', ' ', moby) 
moby_alt = re.sub(r'[\-\'"]+','',moby_exception)


# In[6]:


# This cell tests whether we can access the Moby Dick text as a string
print(moby_alt[:100]) # Change to print only first 100 characters in the string


# ##  Section 3: Using character frequencies to solve coded messages
# Now that we have our sample text downloaded and easy to access, we can try and analyse character frequencies. In Moby Dick and our coded message, we counted the frequency of each character, sorted them by frequency and then tried to cipher them according to how common they were. I.e. the most common character in Moby Dick mapped to the most common in our message. 

# We have utilised Python's built-in function Counter [5] within our own function char_freq to analyse character frequencies. Our function creates two dictionaries, each has keys representing characters and values representing character frequencies. One dictionary corresponds to our large sample text, Herman Melville's Moby Dick and the other corresponds to the inputted string (in this case it is our coded message). 
# After setting up the two dictionaries, we consider any characters not found in the inputted message and append them to the keys of the Decode dictionary, with corresponding frequency values of 0. We assumed that as our sample text is sufficiently large, all 27 characters would appear at least once.
# Following this, we sort both dictionaries by their frequency values into ascending order. This will allow us to make direct comparisons between the frequencies and take an educated guess at which characters are code for which.
# Our function returns both ordered dictionaries.

# In[7]:


# This Python module is used to count the frequencies of characters
from collections import Counter

# Takes a string as input
def char_freq(message):
    
    Sample = dict(Counter(moby_alt)) # Dictionary holding character frequency from large sample text
    Decode= dict(Counter(message)) # Dictionary holding character frequency from coded message
    
    for letter in alphabet: # This deals with characters that do not appear in the message
        if letter not in Decode:
            Decode.update({letter :0})
            
    # This sorts the characters by ascending order by their values
    Sample =  {k:v for k, v in sorted(Sample.items(), key=lambda x:x[1])}
    Decode = {k:v for k, v in sorted(Decode.items(), key=lambda x:x[1])}
    return Sample, Decode    


# In[8]:


# This is a test for char_freq()
print(char_freq(message2))


# In the cell below, we have defined another function called switch(). It implements our function char_freq() and assigns the output of char_freq to the dictionaries Sample and Decode, corresponding to frequencies from the sample text and our message respectively. We then define a new dictionary, corresponding_char, which takes the ordered dictionaries and sets the keys to be the characters from our sample text in ascending order and the matching values to be the characters from our message in ascending order. Effectively, if our code is accurate, each key is the coded character for the character stored in the value.

# In[9]:


def switch(message):
    Sample,Decode = char_freq(message)
    
    # Making a new dictionary that matches each character by frequency
    corresponding_char = {k: v for k, v in zip(Decode.keys(), Sample.keys())}
    return corresponding_char


# Below is our first attempt at our function which will produce our decoded message. The function first_try creates a string called decoded_message, this will hold all the decoded characters in order. It assigns the outputted dictionary from our switch() function to the dictionary cipher [6]. Then for each character in the message, it finds it in the cipher keys, and appends the cipher value to the string. Eventually the for loop terminates and the function returns the decoded message.

# In[10]:


def first_try(message):
    decoded_message = ''
    cipher = switch(message)
    for character in message:
        decoded_message += (cipher[character]) # This appends each decoded character to the string
    return decoded_message


# In[11]:


# This is a test for first_try
print(first_try(message2))


# As you can see from the output above, our function first_try is far from perfect. When inputting the second decoded message, we receive an unreadable piece of text. This is because certain pairs of letters have similar frequencies , making our cipher dictionary inaccurate. Therefore, we need to find a way to interchange them when decoding.

# ##  Section 4: Using a function to swap characters by trial and error.
# We have created a function labelled swap() to help us correct the output from our function first_try. Swap() requires a sample text and 2 characters as input. It uses Python's built-in .replace() [4] function to replace any occurrences of the first character with the second, and vice versa. It does this by using an intermediate character !. As ! does not appear anywhere in the inputted text (see question 2 for our method for removing punctuation), we can replace the second inputted character (ch2) with !. Then we replace any instances of the first character (ch1) with ch2 in our message. And finally, we can replace all ! (originally all instances of ch2) with ch1. Our code then outputs the new message. This function allows us to adjust the cipher by hand until is readable and the message is decoded.

# In[12]:


def swap(text, ch1, ch2):
    text = text.replace(ch2, '!',) # Replaces ch2 with !
    text = text.replace(ch1, ch2) # Replaces ch1 with ch2
    text = text.replace('!', ch1) # Replaces ! with ch1
    return text 


# In[13]:


# This is a test for swap()
test1 = 'abcdefg'
swap(test1,'a','g')


# Now that we have a function that can swap any two characters, we can create a function which uses user input to hand adjust the output from our first_try function. Readable() uses while loops to ensure the user is inputting valid data (i.e. alphabetical characters or space character for swapping). It also allows the user to make as many swaps as they'd like, until they are satisfied with the readability of the decoded message. Within the function readable(), we use the swap function defined above to replace any instances of the first character with the second, and vice versa. the function then outputs the altered message, allowing the user to inspect the changes and make more swaps if necessary.

# We have included a verbose parameter in our input for the function readable(). The verbose parameter if set to True will display all the intermediate versions of the decoded message, after each hand alteration. On the other hand, if verbose is set to False, it will keep asking for input of characters to swap, but will only display the final decoded message. 

# In[49]:


def readable(message,verbose = False):
    updated_message = first_try(message) # This holds the rough attempt at translating the code
    print('This is the first attempt at decoding the message:\n')
    print(updated_message)
    changed = {} # This dictionary holds which characters have been switched so that later the user can see their changes
    if verbose: # If verbose is true, this part of code runs and shows the intermediate steps
        while True:
            while True:
                char1 = input('Please input the character you would like to be replaced: ' )
                char2 = input('Please input the character you would like to be replaced with: ' )
                char1 = char1.upper() # upper() turns the input into upper case characters, it does not affect the space character
                char2 = char2.upper()
                if char1 in alphabet and char2 in alphabet and len(char1)==1 and len(char2)==1:
                    break # this checks that the inputs are only one character each and in our list of allowed characters
                else:
                    print('The input is not valid') # otherwise the while loop asks them to re-enter a valid input
    
            changed.update({char1:char2}) # This appends the swapped characters to the dictionary
            # This uses our swap function to alter the decoded message
            updated_message = swap(updated_message, char1, char2) 
            print(updated_message) # Outputs new message with the swaps made
    
            while True: # This deals with whether the user wants to continue hand adjusting the cipher or is happy with the output
                answer =  input('Would you like to continue? Yes/No: ' )
                if answer not in ['Y','y','Yes','yes','N','n','No','no']:
                    print('That is not a valid option')
                    continue
                else: 
                    break
            
            if answer in ['Y','y','Yes','yes']:
                continue
            else: 
                print('The message is as follows:\n' + updated_message)
                print('The changed characters is as follows' ,changed)
                return(updated_message)
    else: # This part of code runs if verbose is set to False, it does not show the intermediate steps
        while True:
            while True:
                char1 = input('Please input the character you would like to be replaced: ' )
                char2 = input('Please input the character you would like to be replaced with: ' )
                char1 = char1.upper() 
                char2 = char2.upper()
                if char1 in alphabet and char2 in alphabet and len(char1)==1 and len(char2)==1:
                    break 
                else:
                    print('The input is not valid') 
            changed.update({char1:char2}) 
            updated_message = swap(updated_message, char1, char2) 
            while True:
                answer =  input('Would you like to continue? Yes/No: ' )
                if answer not in ['Y','y','Yes','yes','N','n','No','no']:
                    print('That is not a valid option')
                    continue
                else: 
                    break
            
            if answer in ['Y','y','Yes','yes']:
                continue
            else: 
                print('The message is as follows:\n' + updated_message)
                print('The changed characters is as follows' ,changed)
                return(updated_message)   
        


# In[52]:


# Here are the character changes necessary to decode message 2, found by trial and error and using verbose = True
{'F': 'G', 'I': 'H', 'V': 'K', 'N': 'I', 'W': 'U', 'Q': 'X', 'J': 'Z','H':'S','G':'P','U':'F'}


# Above is a dictionary containing the necessary swaps needed to make the output from first_try for message 2 readable. To test our function, input these changes below into readable().

# In[51]:


# This cell allows you to try out our function readable() and make the swaps mentioned below to check our working
readable(message2,True)


# Decoded message 2 reads as follows:
# 
# Sherlock Holmes preserved his calm professional manner until our visitor had left us, although it was easy for me, who knew him so well, to see that he was profoundly excited. The moment that Hilton Cubitt’s broad back had disappeared through the door my comrade rushed to the table, laid out all the slips of paper containing dancing men in front of him, and threw himself into an intricate and elaborate calculation. For two hours I watched him as he covered sheet after sheet of paper with figures and letters, so completely absorbed in his task that he had evidently forgotten my presence. Sometimes he was making progress and whistled and sang at his work; sometimes he was puzzled, and would sit for long spells with a furrowed brow and a vacant eye. Finally he sprang from his chair with a cry of satisfaction, and walked up and down the room rubbing his hands together. Then he wrote a long telegram upon a cable form. “If my answer to this is as I hope, you will have a very pretty case to add to your collection, Watson,” said he, “I expect that we shall be able to go down to Norfolk tomorrow, and to take our friend some very definite news as to the secret of his annoyance.”
# I confess that I was filled with curiosity, but I was aware that Holmes liked to make his disclosures at his own time and in his own way; so I waited until it should suit him to take me into his confidence. But there was a delay in that answering telegram, and two days of impatience followed, during which Holmes pricked up his ears at every ring of the bell. On the evening of the second there came a letter from Hilton Cubitt. All was quiet with him, save that a long inscription had appeared the morning upon the pedestal of the sundial. He enclosed a copy of it, which is here reproduced: 
# Elsie, prepare to meet thy God! 
# Holmes bent over this grotesque frieze for some minutes and then suddenly sprang to his feet with an exclamation of surprise and dismay. His face was haggard with anxiety.
# 
# For readability purposes, we have taken our best guesses at puncuation and capitalisation.

# ## Section 5: Using bigram frequency to solve longer texts

# A bigram is defined as a sequence of two adjacent elements from a string, in our case a bigram is the sequence of any two characters. We compute a probability associated with the likelihood that a specific character will follow from a given character. So, for each bigram i,j we compute <br>
# $p(i,j):=\frac{frequency(ij)+1}{frequency(i)}$. <br>
# This represents the probability that i is followed by j, which allows insight into bigrams that occur frequently in order to decode messages. This also includes spaces. We add one to the numerator of this probability to avoid zeros. For example one of the bigrams of two letters that occured most in the Moby Dick book was HE and TH as expected.

# Within our function bigram, we use the built-in Counter function (which was seen in previous code). We are combining it with a generator expression to slice the sample text string into bigrams [8]. The i:i+2 refers to a substring consisting of the character at index i and the charcter at index i+1. This is where the Counter function comes in, as it counts the number of occurrences of this substring. We use a for in loop to analyse each bigram in the sample text and to calculate it's frequency. The range is 0 to len(message)-1 as the last bigram is analysed using i = len(message)-1 and i+1 = len(message). 

# In[1]:


def bigram_freq(text):
    # Stores bigrams and their frequency in a dictionary
    bigram_dict = dict(Counter(text[i : i + 2] for i in range(len(text) - 1)))
    probability = {} # Dictionary used to store the p(i,j) values from sample text
    Sample = dict(Counter(text)) # Dictionary holding character frequency from large sample text
    for key in bigram_dict: # Iterates through each bigram
        # We need to split bigram, take the first character, and get its character frequency from the sample 
        bigram_split = list(key) 
        f = Sample.get(bigram_split[0]) # [7] This returns the frequency of the character by finding the key's value in the dictionary
        p = (bigram_dict[key] +1)/f # This is the p(i,j) value 
        probability.update({key:p})
    return probability


# In[19]:


# This cell is for testing bigram_freq()
text = 'ABRACADABRA'
bigram_freq(text)

# In the output of this cell, you will see that because of the +1 in the formula for p(i,j) we can get p values ranging 
# from (0,2].


# In[20]:


# This tests how many distinct bigrams appear in first 20 characters of Moby Dick
bigram_freq(moby_alt[:20])


# We now have the probability of all the bigrams that occured in Moby Dick. This will be used to score a piece of text on how likely it is to be English. One slight problem we encountered was that our bigram frequency function did not account for all $27^{2}$ = 729 bigrams, hence we added the missing bigrams that did not occur in Moby Dick so that we can later use them for the Metropolis algorithm. If a bigram does not appear in Moby Dick, it was assigned a $frequency(ij)$ of 0.
# 

# In[55]:


import numpy as np # This module is imported so we can use the built-in log function

log_dict = bigram_freq(moby_alt) # This stores the result from our p(i,j) functions for all bigrams that appear in moby dick

#This deals with bigrams not in moby dick
all_bigrams = []
for i in alphabet:
    for j in alphabet: # Here we concatenate the 2 characters to form a bigram, this creates 729 unique bigrams
        bigram = i+j
        all_bigrams.append(bigram)


# Checks if a bigram appears in Moby Dick, if not, assigns it a a freq of 0 and finds resulting p(i,j) value and adds it to 
# the log_dict
Sample = dict(Counter(moby_alt))
for x in all_bigrams:
    if x in log_dict: # It is in Moby Dick, so nothing further needs to be done
        continue
    else: # It is not found in Moby Dick, need to add a p(i,j) value
        bigram_split = list(x) 
        f = Sample.get(bigram_split[0]) 
        p = 1/f 
        log_dict.update({x:p})

for key in log_dict: 
    log_dict.update({key:np.log(log_dict[key])}) # We then take the log of all the p(i,j) values and update the dictionary


# Now that we have a probability of all bigrams, we can code in a function called plausibility_score that will compute a score for any text m. This is going to be later used in the Metropolis algorithm. First it calculates the logarithm of the probability of each bigram that occurs in a text in chronological order, and sums it from the first character to the character before the last. This then gives the plausibility score.

# In[22]:


def plausibility_score(message):
    # split message into bigrams
    #takes each bigram in the message and finds it in logdict
    #then adds it to the score counter
    score = 0 # This variable will hold the sum of each log(p(i,j))
    message_bigrams = [message[i : i + 2] for i in range(len(message) - 1)] # Stores all the bigrams as strings in a list
    for i in message_bigrams: # adds the score for each bigram in the message to the total score
        score += log_dict.get(i)
    return score


# In[23]:


# This cell is a test for our S(m) function called plausibility_score()
text = 'ABRACADABRA'
plausibility_score(text)


# ##  Section 6: Using the Plausibility score and Metropolis algorithm

# 
# We want our code to self-improve the message, working towards getting a better plausibility score. To do this we implemented the Metropolis algorithm (an example of a Monte Carlo method). The Metropolis algorithm is a method in statistical physics used to obtain a sequence of random samples from a probability distribution of which direct sampling is difficult. At each iteration, the Metropolis algorithm picks a random value for the next sample value based on the current sample value, then with some probability the random value is either accepted and used for the next iteration or discarded and the current value is used for the next iteration. The probability of acceptance is determined by comparing the values of the function of the current and random value with respect to the desired distribution.
# In our case this probability distribution is our bigram frequency, and we developed this method by starting with our first_try output as our first guess $m$ at the decrypted message. Next we instructed the algorithm to choose two characters at random [9] and swap their roles in the cipher, to get a new candidate
# message $m^{'}$.
# - If $S(m^{'}) > S(m)$ then replace $m$ with $m^{'}$
# - If $S(m^{'}) ≤ S(m)$ then replace $m$ with $m^{'}$ with probability : $exp(\frac{S(m^{'})-S(m)}{T})$
# 
# We ran this code for n = 10000 times so that the algorithm had sufficient time to alter the message to make it more readable.
# T is a parameter representing how likely the algorithm is to accept steps which make the message less readable, in hopes of finding a better path to the answer later on. A small T value is unlikely to accept a less readable message, whereas larger T values would.

# In[24]:


# introduction to metropolis


# In[25]:


import random
import math

def metropolis(message,T):
    # Here we start off with our first_try function from above as our first decrypted message.
    start = first_try(message)
    print(start)
    for n in range(10000):
        Sm0 = plausibility_score(start)
        #randomly pick 2 letters in alphabet list (no rep)
        ch1 = random.choice(alphabet)
        while True: # Keeps choosing a random character until one is selected which is distinct from character 1
            ch2 = random.choice(alphabet)
            if ch2 != ch1:
                break
        new_message = swap(start,ch1,ch2) # This swaps the 2 characters in the message
        Sm1 = plausibility_score(new_message) # Assigns a plausibility score to the new message
        # replaces new message with old if new is more plausible
        if Sm1 > Sm0:
            start = new_message
        else:
            prob = math.exp((Sm1-Sm0)/T) # This is the probability that we replace the 
            # old message with the new even though it has a lower plausibility score
            random_float = random.random() # This generates a random float in [0,1] with uniform distribution
            if random_float <= prob: # Replaces old message
                start = new_message
            else: # Does not change the message
                continue
    return start


# Using the Metropolis function and varying T values we decrypted messages 3,4,5,6,7 and 8. We had to run the function numerous times and hand adjust the cipher slightly.

# In[56]:


# This cell is a test for metropolis
metropolis(message9,1)


# The above output is unreadable so we must adjust our code somehow. Below we adapted the metropolis function to use simulated annealing. This is where T takes an initial value of 10 but gradually decreases by a constant ratio so that finally we reach T=0.1. This means as the algorithm progresses, it is less likely to accept a version of the message which makes it less readable. This makes it so that there is less human intervention and the program can run through T values.

# In[27]:


def metropolis_ext(message):
    start = first_try(message)
    print(start)
    T = 10
    a = 0.01**(1/100)
    for n in range(10000):
        if n%100 == 0: # Every 100 steps, T decreases by a constant ratio a
            T = T*a
        Sm0 = plausibility_score(start)
        #randomly pick 2 letters in alphabet list (no rep)
        ch1 = random.choice(alphabet)
        while True: # Keeps choosing a random character until one is selected which is distinct from character 1
            ch2 = random.choice(alphabet)
            if ch2 != ch1:
                break
        new_message = swap(start,ch1,ch2) # This swaps the 2 characters in the message
        Sm1 = plausibility_score(new_message) # Assigns a plausibility score to the new message
        # replaces new message with old if new is more plausible
        if Sm1 > Sm0:
            start = new_message
        else:
            prob = math.exp((Sm1-Sm0)/T) # This is the probability that we replace the 
            # old message with the new even though it has a lower plausibility score
            random_float = random.random() # This generates a random float in [0,1] with uniform distribution
            if random_float <= prob: # Replaces old message
                start = new_message
            else: # Does not change the message
                continue
    return start


# In[57]:


# This is a test cell for the extended metropolis function
metropolis_ext(message9)


# Still this code looks unreadable in English, however some of the word lengths and sentence structures resemble those in the French language. Therefore, we shall write a new piece of code which uses a large piece of French text instead for it's sample text. We decided to use The Count of Monte Cristo, and shall write a text file in the same way we created one for Moby Dick.

# In[29]:


link = "https://www.gutenberg.org/cache/epub/17989/pg17989.txt"
monte = requests.get(link).text
with open('monte.txt','w',errors='ignore') as f:
    f.write(monte.upper()) # write to file

# This code opens our pre-made text file and reads it into a string variable called monte
with open('monte.txt','r',errors='ignore',encoding = 'utf-8') as f:
    monte=f.read() 
    
# Here we deal with non alphabetical characters and those that aren't white spaces.
monte_exception = re.sub(r'[^A-Z\-\'"]+', ' ', monte) 
monte_alt = re.sub(r'[\-\'"]+','',monte_exception)


# As a lot of our previous code incorporated the analysis of Moby Dick, we must adjust these functions so that they instead use The Count of Monte Cristo.

# In[58]:


# Inputting a different sample text into the bigram_freq function
log_dict_french = bigram_freq(monte_alt) 

all_bigrams = []
for i in alphabet:
    for j in alphabet: 
        bigram = i+j
        all_bigrams.append(bigram)

Sample = dict(Counter(monte_alt))
for x in all_bigrams:
    if x in log_dict_french: 
        continue
    else: 
        bigram_split = list(x) 
        f = Sample.get(bigram_split[0]) 
        p = 1/f 
        log_dict_french.update({x:p})

for key in log_dict_french: 
    log_dict_french.update({key:np.log(log_dict_french[key])}) 

# Altering the plausibility score function to use the french log dictionary
def plausibility_score_french(message):
    message_bigrams = [message[i : i + 2] for i in range(len(message) - 1)] 
    score = 0
    for i in message_bigrams: 
        score += log_dict_french.get(i)
    return score

# Making sure the metropolis extended function uses the french plausibility function
def metropolis_ext_french(message):
    start = message # This has also been adjusted to use just the initial message rather than the first try output
    print(start)
    T = 10
    a = 0.01**(1/100)
    for n in range(10000):
        if n%100 == 0: 
            T = T*a
        Sm0 = plausibility_score_french(start)
        ch1 = random.choice(alphabet)
        while True: 
            ch2 = random.choice(alphabet)
            if ch2 != ch1:
                break
        new_message = swap(start,ch1,ch2) 
        Sm1 = plausibility_score_french(new_message) 
        if Sm1 > Sm0:
            start = new_message
        else:
            prob = math.exp((Sm1-Sm0)/T)  
            random_float = random.random() 
            if random_float <= prob: 
                start = new_message
            else: 
                continue
    return start


# In[31]:


#Test cell for french version
metropolis_ext_french(message9)


# As we can see above, once we substituted a French text into the functions we defined before, we were able to use the Metropolis function to decypher the code. 

# ## Section 7: Decoded Messages
# Below are all the messages we were able to decode, with our best guess at capitalisation and punctuation:
# 
# Message 1:
# Python is an interpreted, high level and general purpose programming language. Python's design philosophy empahsizes code readability with its notable use of signifcant identation. Its language constucts and object oriented approach aim to help programmers write clear, logical code for small and large scale projects.
# 
# Message 2:
# Sherlock Holmes preserved his calm professional manner until our visitor had left us, although it was easy for me, who knew him so well, to see that he was profoundly excited. The moment that Hilton Cubitt’s broad back had disappeared through the door my comrade rushed to the table, laid out all the slips of paper containing dancing men in front of him, and threw himself into an intricate and elaborate calculation. For two hours I watched him as he covered sheet after sheet of paper with figures and letters, so completely absorbed in his task that he had evidently forgotten my presence. Sometimes he was making progress and whistled and sang at his work; sometimes he was puzzled, and would sit for long spells with a furrowed brow and a vacant eye. Finally he sprang from his chair with a cry of satisfaction, and walked up and down the room rubbing his hands together. Then he wrote a long telegram upon a cable form. “If my answer to this is as I hope, you will have a very pretty case to add to your collection, Watson,” said he, “I expect that we shall be able to go down to Norfolk tomorrow, and to take our friend some very definite news as to the secret of his annoyance.” I confess that I was filled with curiosity, but I was aware that Holmes liked to make his disclosures at his own time and in his own way; so I waited until it should suit him to take me into his confidence. But there was a delay in that answering telegram, and two days of impatience followed, during which Holmes pricked up his ears at every ring of the bell. On the evening of the second there came a letter from Hilton Cubitt. All was quiet with him, save that a long inscription had appeared the morning upon the pedestal of the sundial. He enclosed a copy of it, which is here reproduced: Elsie, prepare to meet thy God! Holmes bent over this grotesque frieze for some minutes and then suddenly sprang to his feet with an exclamation of surprise and dismay. His face was haggard with anxiety.
# 
# Message 3:
# Ciphertexts produced by a classical cipher (and some modern ciphers) will reveal statistical information about the plaintext and that information can often be used to break the cipher. After the discovery of frequency analysis by the Arab mathematician and polymath, Al-Kindi (also known as Alkindus), in the ninth century, nearly all such ciphers could be broken by an informed attacker. Such classical ciphers still enjoy popularity today, though mostly as puzzles. Al-Kindi wrote a book on cryptography entitled Risalah fi Istikhraj al-Mu'amma (Manuscript for the Deciphering Cryptographic Messages), which described the first known use of frequency analysis and cryptanalysis techniques. An important contribution of Ibn Adlan was on sample size for use of frequency analysis. 
# 
# Message 4:
# Working with their Egyptian colleagues, the Dutch consultants were running numbers. Boskalis’s role was basically to do the calculations the sums Berdowski said, so when the stern came free on Monday morning, we calculated that we should let tonnes of water ballast in at the rear of the vessel to push the stern down and lift the bow. 
# 
# Message 5:
# A very choice monkey was taken ill and refused to eat. It was thought however, that it’s appetite might be stimulated by a pineapple.   
# 
# Message 6:
# Tatterdemalion and then a junketer 
# There's a thief and a dragonfly trumpeter 
# He's my hero 
# Fairy dandy tickling the fancy 
# Of his lady friend 
# The nymph in yellow 
# 'Can we see the master stroke' 
# What a quaere fellow 
# 
# Message 7:
# From the beginning think what may be the end. 
# 
# Message 8:
# Amang the trees, where humming bees 
# At buds and flowers were hinging, O, 
# Auld Caledon drew out her drone, 
# And to her pipe was singing, O. 
# 'Twas Pibroch, Sang, Strathpeys, and Reels, 
# She dirl'd them aff fu' clearly, O, 
# When there cam a yell o' foreign squeels, 
# That dang her tapsalteerie, O! 
# 
# Message 9:
# Je me rendormais, et parfois je n'avais plus que de courts réveils d'un instant, le temps d'entendre les craquements organiques des boiseries, d'ouvrir les yeux pour fixer le kaléidoscope de l'obscurité, de goûter grâce à une lueur momentanée de conscience le sommeil où étaient plongés les meubles, la chambre, le tout dont je n'étais qu'une petite partie et à l'insensibilité duquel je retournais vite m'unir. 

# ## Conclusion 
# 
# Throughout this project on code breaking with statistical physics, we have used a combination of Caesar cipher shifts, analysis of character frequencies and the Metropolis method to decypher messages. These methods have proved to be very effective and needed little human intervention. Due to time pressures and difficulty of the coded messages we weren't able to decode some of the shorter messages or explore using trigrams. The implementation of trigram analysis would have made decoding the shorter messages significantly easier if common trigrams such as 'and' or 'the' appeared. If provided more time we could have inputted some common trigrams manually and checked whether this would have helped us solve the later messages. Additionally, we could have improved our algorithm by using a longer text that included all 729 bigrams or analysing texts in other languages earlier on, this would have increased the speed of which we decoded message 9. 

# # Bibliography:
# ### [1] Stack Overflow. 2014. *How to make a Caesar Cipher work*
# Available at: https://stackoverflow.com/questions/20269330/how-to-make-a-caesar-cipher-work-with-input-that-has-spaces-in-python
# Accessed : 16/5/2021
# 
# ### [2] Python Docs. 2021. *Regular expression operations*
# Available at: https://docs.python.org/3/library/re.html
# Accessed : 16/5/2021
# 
# ### [3] LZone. *Regular expression examples*
# Available at: https://lzone.de/examples/Python%20re.sub
# Accessed : 16/5/2021
# 
# ### [4] Note.Nkmk. 2019. *Replace strings in Python*
# Available at: https://note.nkmk.me/en/python-str-replace-translate-re-sub/
# Accessed : 16/5/2021
# 
# ### [5] Journaldev. *Python counter*
# Available at: https://www.journaldev.com/20806/python-counter-python-collections-counter
# Accessed : 16/5/2021
# 
# ### [6] L. Ramos. *How to iterate through dictionaries* Real Python
# Available at: https://realpython.com/iterate-through-dictionary-python/#iterating-through-keys-directly
# Accessed : 16/5/2021
# 
# ### [7] Programwiz. *Python Dictionary get()*
# Available at: https://www.programiz.com/python-programming/methods/dictionary/get
# Accessed : 16/5/2021
# 
# ### [8] GeeksForGeeks. 2020. *Bigrams Frequencies in string*
# Available at: https://www.geeksforgeeks.org/python-bigrams-frequency-in-string/
# Accessed : 16/5/2021
# 
# ### [9] Stack Overflow. 2009. *How to randomly select an item from a list?*
# Available at: https://stackoverflow.com/questions/306400/how-to-randomly-select-an-item-from-a-list 
# Accessed : 16/5/2021
