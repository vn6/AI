import nltk
from nltk.corpus import conll2000

print("3. Pick one of the three chunk types in the CoNLL corpus. "
      "Inspect the CoNLL corpus and try to observe any patterns in the POS tag sequences that "
      "make up this kind of chunk. Develop a simple chunker using the regular expression chunker nltk.RegexpParser. "
      "Discuss any tag sequences that are difficult to chunk reliably.")

print("7. Carry out the following evaluation tasks for any of the chunkers you have developed earlier. "
      "(Note that most chunking corpora contain some internal inconsistencies, "
      "such that any reasonable rule-based approach will produce errors.)"
      "a. Evaluate your chunker on 100 sentences from a chunked corpus, and report the precision, recall and F-measure."
      "b. Use the chunkscore.missed() and chunkscore.incorrect() methods to identify the errors made by your chunker. Discuss."
      "c. Compare the performance of your chunker to the baseline chunker discussed in the evaluation section of this chapter.")

GRAMMAR = r"""NP: {<DT>?<POS>?<RB>?<PRP.*>?<CD.*>*<JJ.*>*<NN.*>+}
                  {<DT>?<POS>?<VB.*>*<JJ.*>*<NN.*>+}
                  {<DT>?<NN.*>+<CC><NN.*>+}
                  {<IN><CD><NN.*>+}
                  {<PRP>}
                  {<WP>}
                  {<WDT>}
                  """
CP = nltk.RegexpParser(GRAMMAR)
TEST_SENTS = conll2000.chunked_sents('test.txt', chunk_types=['NP'])


def evaluate_chunker():
    print(CP.evaluate(TEST_SENTS))
    chunkscore = nltk.chunk.ChunkScore()
    for x in range(0,99):
        test_text = conll2000.chunked_sents('train.txt', chunk_types=['NP'])[x]
        chunked_text = CP.parse(test_text.flatten())
        chunkscore.score(test_text, chunked_text)
    print(chunkscore.accuracy())
    for chunk in sorted(chunkscore.missed()):
        print(chunk)
    print("--------------------------------------")
    for chunk in sorted(chunkscore.incorrect()):
        print(chunk)
evaluate_chunker()
