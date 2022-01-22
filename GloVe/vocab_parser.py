import sys

def read_text(filename):
    file = open(filename, mode='rt', encoding='ISO-8859-1')
    text = file.read()
    file.close()
    return text


def to_lines_vocab(text):
    vocab_list = [];
    vocab_string = "";
    sents = text.strip().split('\n')
    for sent in sents:
        if sent.strip() == "":
            continue
        sent_tokenized = sent.split(' ')
        try:
            #print("Hello vocab")
            vector = sent_tokenized[1:]
            if len(vector) == 512 and sent_tokenized[0].strip() != "":
                vocab_list.append(sent_tokenized[0])
                vocab_string = vocab_string + sent_tokenized[0].strip() + '\n';
            else:
                print("@@@")
        except:
            print("Something went wrong vocab ", sys.exc_info()[0])
        
        if len(vocab_list) >= 30000:
            break
    return vocab_string;

def to_lines_vector(text):
    vocab_list = [];
    vocab_string = "";
    sents = text.strip().split('\n')
    for sent in sents:
        if sent.strip() == "":
            continue
        sent_tokenized = sent.split(' ')
        try:
            #print("Hello vector")
            vector = sent_tokenized[1:]
            if len(vector) == 512 and sent_tokenized[0].strip() != "":
                vocab_list.append(sent_tokenized[0])
                vocab_string = vocab_string + sent.strip() + '\n';
            else:
                print("###")
        except:
            print("Something went wrong vector ", sys.exc_info()[0])
        
        if len(vocab_list) >= 30000:
            break
    return vocab_string;

if __name__ == '__main__':

    
    xdata = read_text("vectors.txt");
    vocab_string = to_lines_vocab(xdata);

    with open("vocab_parsed.txt", 'w') as outfile:
          outfile.write(str(vocab_string))
    vocab_string = ""

    vocab_string = to_lines_vector(xdata);
    with open("vectors_parsed.txt", 'w') as outfile:
          outfile.write(str(vocab_string))



