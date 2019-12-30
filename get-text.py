from convert import read_lines, write_lines

STANFORD_FILE = 'stanford-ner-corpus.txt'

tokens = [line.split(' ')[0] for line in read_lines(STANFORD_FILE)]

write_lines('text.txt', [' '.join(tokens),])