from convert import read_lines, write_lines

STANFORD_POS_FILE = 'ru-conll2003.txt'
STANFORD_FILE = 'stanford-ner-corpus.txt'
POS_FILE = 'phrase_types.txt'

tokens_with_entities = [line.split(' ') for line in read_lines(STANFORD_FILE)]
tokens_with_pos_and_phrase_types = [line.split(' ') for line in read_lines(POS_FILE)[:-1]]

write_lines(STANFORD_POS_FILE, list([' '.join([pair[0][0], pair[1][2], pair[1][1], pair[0][1]]) for pair in zip(tokens_with_entities, tokens_with_pos_and_phrase_types)]))
#write_lines('stanford-ner-corpus-pos.txt', [' '.join(tokens),])