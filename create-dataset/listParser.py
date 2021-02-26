import sys
import math

rawCode = {}

num_of_chunks = 4

def read_text(filename):
    file = open(filename, mode='rt', encoding='ISO-8859-1')
    text = file.read()
    file.close()
    return text

def to_chunks(text):
    files = text.strip().split('\n')
    chunk_list = [*range(1, num_of_chunks + 1, 1)] 
    chunk_list_size = len(chunk_list)

    for chunk in chunk_list:
        file = open(foldername + '/chunk_' + str(chunk) + '.txt', 'w')

        for one_file in files[math.floor((chunk-1)/chunk_list_size*len(files)) : math.floor((chunk)/chunk_list_size*len(files))]:
            file.write("%s\n" % one_file)

        file.close()

if __name__ == '__main__':

    filename = sys.argv[1]
    foldername = sys.argv[2]
    data = read_text(filename)
    to_chunks(data)


