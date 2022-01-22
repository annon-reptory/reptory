import sys
import nltk
import io

nltk.download('punkt')

# threshold = 1
threshold = int(sys.argv[1])
vocab_size = int(sys.argv[2])

input_file = io.open('./Vocab/VocabCorpus.correct', mode='r', encoding="utf-8")
correct_code_corpus = input_file.read()

allWords = nltk.tokenize.word_tokenize(correct_code_corpus)
allWordDist = nltk.FreqDist(w for w in allWords)
mostCommon = allWordDist.most_common(vocab_size)

words = [i[0].encode('utf-8') for i in mostCommon if i[1] >= threshold]

output_file = open('./Vocab/vocab.correct', 'w')
for word in words:
  if len(str(word)) > 1 or (not str(word).isdigit() and not str(word).isalpha()):
    output_file.write(word.decode('utf-8') + '\n')

input_file = io.open('./Vocab/VocabCorpus.buggy', mode='r', encoding="utf-8")
buggy_code_corpus = input_file.read()

allWords = nltk.tokenize.word_tokenize(buggy_code_corpus)
allWordDist = nltk.FreqDist(w for w in allWords)
mostCommon = allWordDist.most_common(vocab_size)
words = [i[0].encode('utf-8') for i in mostCommon if i[1] >= threshold]

output_file = open('./Vocab/vocab.buggy', 'w')
for word in words:
  if len(str(word)) > 1 or (not str(word).isdigit() and not str(word).isalpha()):
    output_file.write(word.decode('utf-8') + '\n')
