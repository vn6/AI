import random

import math
from _pydecimal import Decimal

import nltk
from nltk.corpus import gutenberg
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
TEST_TEXT = tokenizer.tokenize(gutenberg.raw(gutenberg.fileids()[0]))

print('7. The word however, used at the start of a sentence, means "in whatever way" or "to whatever extent", '
      'and not "nevertheless". Use the concordance tool to study actual usage of this word '
      'in the various texts we have been considering.')


def however_usage():
    files = gutenberg.fileids()
    for f in files:
        text = nltk.Text(gutenberg.words(f))
        text.concordance("However")

# however_usage()

print()
print('9. Pick a pair of texts and study the differences between them, in terms of vocabulary, '
      'vocabulary richness, genre, etc. Can you find pairs of words which have quite different meanings '
      'across the two texts, such as monstrous in Moby Dick and in Sense and Sensibility?')


def compare_texts():
    emma = gutenberg.fileids()[0]
    leaves = gutenberg.fileids()[-1]
    words1 = gutenberg.words(emma)
    words2 = gutenberg.words(leaves)
    print("Text 1: Emma, Text 2: Leaves")
    print("Length: " + str(len(gutenberg.raw(emma))) + ", " + str(len(gutenberg.raw(leaves))))
    print("Avg Sentence Length: " + str(len(words1)/len(gutenberg.sents(emma))) + ", "
          + str(len(words2)/len(gutenberg.sents(leaves))))
    vocab1 = set([w.lower() for w in words1])
    vocab2 = set([w.lower() for w in words2])
    print("Unique Vocab: " + str(len(vocab1)) + ", " + str(len(vocab2)))
    print("Avg Word Repitition: " + str(len(words1)/len(vocab1)) + ", " + str(len(words2)/len(vocab2)))
    nltk.Text(gutenberg.words(emma)).concordance("leaves")
    nltk.Text(gutenberg.words(leaves)).concordance("leaves")
    return

# compare_texts()

print()
print('12 The CMU Pronouncing Dictionary contains multiple pronunciations for certain words. '
      'How many distinct words does it contain? '
      'What fraction of words in this dictionary have more than one possible pronunciation?')


def cmu_stats():
    cmu_entries = nltk.corpus.cmudict.entries()
    unique_words = set()
    mult_pron_count = 0
    mult_pron_words = set()
    for word, pron in cmu_entries:
        if word not in mult_pron_words and word in unique_words:
            mult_pron_count += 1
            mult_pron_words.add(word)
        else:
            unique_words.add(word)
    return len(unique_words), len(mult_pron_words)/len(unique_words)

# res = cmu_stats()
# print("Unique Words: " + str(res[0]))
# print("Fraction of Words with Multiple Pronunciations: " + str(res[1]))

print()
print('13. What percentage of noun synsets have no hyponyms?')


def hyponym_percent():
    all_words = 0
    no_hyponyms = 0
    for synset in wn.all_synsets('n'):
        all_words += 1
        if  not synset.hyponyms():
            no_hyponyms += 1
    return no_hyponyms/all_words

# print(hyponym_percent())

print()
print('15. Write a program to find all words that occur at least three times in the Brown Corpus.')


def brown_words():
    all_words = brown.words()
    fdist = nltk.FreqDist(w.lower() for w in all_words)
    return [word for word in fdist if fdist[word]>=3]

# print(brown_words())

print()
print('17. Write a function that finds the 50 most frequently occurring words of a text that are not stopwords.')


def freq_words(text):
    stop_words = stopwords.words('english')
    content = [w for w in text if w.lower() not in stop_words]
    fdist =  nltk.FreqDist(w.lower() for w in content)
    top_words = sorted(fdist.keys(), key=lambda x: -fdist[x])
    return top_words[:50]

print(str(freq_words(TEST_TEXT)))

print()
print("23. Zipf's Law: Let f(w) be the frequency of a word w in free text. "
      "Suppose that all the words of a text are ranked according to their frequency, with the most frequent word first. "
      "Zipf's law states that the frequency of a word type is inversely proportional to its rank "
      "(i.e. f × r = k, for some constant k). For example, the 50th most common word type should occur "
      "three times as frequently as the 150th most common word type. \n\t"
      "a. Write a function to process a large text and plot word frequency against word rank using pylab.plot. "
      "Do you confirm Zipf's law? (Hint: it helps to use a logarithmic scale). "
      "What is going on at the extreme ends of the plotted line? \n\t"
      "b. Generate random text. Then tokenize this string, and generate the Zipf plot as before, "
      "and compare the two plots.What do you make of Zipf's Law in the light of this?")


def plot_word_freq(text):
    fdist =  nltk.FreqDist(w.lower() for w in text)
    word_rank = sorted(fdist.keys(), key=lambda x: -fdist[x])
    x = []
    y = []
    for a in range(len(word_rank)):
        x += [a + 1]
        y += [fdist[word_rank[a]]]
        # y += [fdist[word_rank[a]]]
    plt.plot(x, y)
    plt.xlabel('Word Rank')
    plt.ylabel('Frequency')
plt.figure(0)
plot_word_freq(TEST_TEXT)
# plt.show()


def random_text():
    ch = "abcdefghijklmnopqrstuvwxyz "
    s = ""
    for x in range(200000):
        s += random.choice(ch)
    return s.split(" ")

plt.figure(1)
plot_word_freq(random_text())
# plt.show()

print()
print("26. What is the branching factor of the noun hypernym hierarchy? "
      "I.e. for every noun synset that has hyponyms — or children in the hypernym hierarchy — "
      "how many do they have on average? You can get all noun synsets using wn.all_synsets('n').")


def branching_factor():
    num_words = 0
    total_branches = 0
    for synset in wn.all_synsets('n'):
        hyponyms = len(synset.hyponyms())
        if hyponyms > 0:
            num_words += 1
            total_branches +=  hyponyms
    return total_branches / num_words

# print(branching_factor())

plt.show()