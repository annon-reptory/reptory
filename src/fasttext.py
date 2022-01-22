# import nltk
import sys
import nltk
# nltk.download('punkt')
from nltk import word_tokenize, sent_tokenize
from gensim.models import FastText

vocab_size = 30000
minCount = 2
embedding_size = 512
window_size = 20

if __name__ == '__main__':
    tokenized_file = sys.argv[1]
    output_vocab_filename = sys.argv[2]
    output_embed_filename = sys.argv[3]

    f = open(tokenized_file, "r")
    article_text = f.read()

    processed_article = article_text
    # Preparing the dataset
    all_sentences = nltk.sent_tokenize(processed_article)

    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
    fast_text = FastText(sentences=all_words,
                         min_count=minCount,
                         window=window_size / 2,
                         size=embedding_size,
                         workers=40,
                         sg=0)

    vocab_dict = {}
    for word, vocab_obj in fast_text.wv.vocab.items():
        vocab_dict[word] = vocab_obj.count

    sorted_vocab_dict = sorted(vocab_dict.items(), key=lambda item: item[1], reverse=True)
    top_vectors = ""
    top_tokens = ""
    counter = 0

    for word in sorted_vocab_dict:
        if counter == vocab_size:
            break
        vector = ' '.join(map(str, fast_text.wv[word[0]]))
        top_tokens = top_tokens + word[0] + "\n"
        top_vectors = top_vectors + word[0] + " " + vector + "\n"
        counter += 1

    with open(output_vocab_filename, 'w') as outfile:
        outfile.write(top_tokens)

    with open(output_embed_filename, 'w') as outfile:
        outfile.write(top_vectors)
