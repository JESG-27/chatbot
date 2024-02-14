import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
stemmer = PorterStemmer()

# Delete line after first run
#nltk.download('punkt')

def tokenize(sentence):
    return nltk.word_tokenize(sentence);

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentece, all_words):
    tokenized_sentece = [stem(w) for w in tokenized_sentece]
    bow = np.zeros(len(all_words), dtype=np.float32)
    for ind, w in enumerate(all_words):
        if w in tokenized_sentece:
            bow[ind] = 1.0

    return bow
    
'''
Uncomment to print how tokenization works
a = 'OMG, It is amazing!'
print(a)
a = tokenize(a)
print(a)
'''

'''
Uncomment to print how stemming works
words = ['Organize', 'organizes', 'organizing']
final = [stem(i) for i in words]
print(final)
'''