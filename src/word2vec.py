import nltk
import smart_open
smart_open.open = smart_open.smart_open
from gensim.models import Word2Vec
import argparse

vocab_size = 30000
minCount = 2
embedding_size = 512
window_size = 20

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generate word2vec embedding')

    parser.add_argument("tokenized_file", type=str)
    parser.add_argument("output_vocab_filename", type=str)
    parser.add_argument("output_embed_filename", type=str)
    parser.add_argument("embedding_size", type=int)
    parser.add_argument("--vocab_size", type=int, required=False, default=30000)

    args = parser.parse_args()
    tokenized_file = args.tokenized_file  # sys.argv[1]
    output_vocab_filename = args.output_vocab_filename  # sys.argv[2]
    output_embed_filename = args.output_embed_filename  # sys.argv[3]
    embedding_size = args.embedding_size  # int(sys.argv[4])
    vocab_size = args.vocab_size

    print("hyperparameter setting for word2vec={0}".format(args))
    print("running word2vec with embedding_size={0}".format(embedding_size))

    f = open(tokenized_file, "r")
    article_text = f.read()

    processed_article = article_text
    all_sentences = nltk.sent_tokenize(processed_article)

    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
    word2vec = Word2Vec(all_words, min_count=minCount, window=window_size/2, size=embedding_size, workers=40)

    vocab_dict = {}
    for word, vocab_obj in word2vec.wv.vocab.items():
        vocab_dict[word] = vocab_obj.count

    sorted_vocab_dict = sorted(vocab_dict.items(), key=lambda item: item[1], reverse=True)
    top_vectors = ""
    top_tokens = ""
    counter = 0

    for word in sorted_vocab_dict:
        if counter == vocab_size:
            break
        vector = ' '.join(map(str, word2vec.wv[word[0]]))
        top_tokens = top_tokens + word[0] + "\n";
        top_vectors = top_vectors + word[0] + " " + vector + "\n";
        counter += 1

    with open(output_vocab_filename, 'w') as outfile:
        outfile.write(top_tokens)

    with open(output_embed_filename, 'w') as outfile:
        outfile.write(top_vectors)
