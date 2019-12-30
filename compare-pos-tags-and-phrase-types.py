from convert import read_lines, write_lines

POS_FILE = 'stanford-ner-corpus.txt'
PHRASE_TYPES_FILE = 'phrase_types.txt'

pos_tokens = list(map(lambda line: line.split(' ')[0], read_lines(POS_FILE)))
phrase_types = list(map(lambda line: line.split(' ')[0], read_lines(PHRASE_TYPES_FILE)))

counter = 1000
for i in range(len(pos_tokens)):
	if pos_tokens[i] != phrase_types[i]:
		counter -= 1
		print(i, pos_tokens[i], phrase_types[i])
	if (counter < 0):
		break