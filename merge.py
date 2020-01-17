from convert import read_lines, write_lines
import argparse, random

parser = argparse.ArgumentParser()

TRAIN_FILE = 'conll2003ru/train.txt'
TEST_FILE = 'conll2003ru/test.txt'
DEV_FILE = 'conll2003ru/dev.txt'

parser.add_argument('--train', type=float, default=0.7)
parser.add_argument('--test', type=float, default=0.2)

args = parser.parse_args()

structure_stanford_deps = __import__('structure-stanford-deps')

STANFORD_POS_FILE = 'ru-conll2003.txt'
STANFORD_FILE = 'stanford-ner-corpus.txt'
POS_FILE = 'phrase_types.txt'

tokens_with_entities = [line.split(' ') for line in read_lines(STANFORD_FILE)]
tokens_with_pos_and_phrase_types = [line.split(' ') for line in read_lines(POS_FILE)[:]]

# Add bio prefixes for entities labels
no_entity_mark = 'O'
previous_entity = ''
new_tokens_with_entities = []
for token, entity in tokens_with_entities:
	new_tokens_with_entities.append((token, f'{structure_stanford_deps.get_bio_prefix(previous_entity, entity) if entity != no_entity_mark else ""}{entity}'))
	previous_entity = entity
tokens_with_entities = new_tokens_with_entities

def flatten_sentences(sentences):
	flattened = []
	for sentence in sentences:
		for line in sentence:
			flattened.append(line)
		flattened.append('')
	return flattened

def write_sentences(sentences, filename, preamble):
	write_lines(filename, preamble + flatten_sentences(sentences))

#Merge
preamble = list(map(lambda item: ' '.join(item), tokens_with_pos_and_phrase_types[:2]))
sentences = []
sentence = []
i = 2
for token, entity in tokens_with_entities:
	were_deleted_empty_lines = False
	if i >= len(tokens_with_pos_and_phrase_types):
		break
	while len(tokens_with_pos_and_phrase_types[i]) == 1:
		#print(tokens_with_pos_and_phrase_types[i])
		i += 1
		if not were_deleted_empty_lines:
			were_deleted_empty_lines = True
	if were_deleted_empty_lines:
		sentences.append(sentence)
		sentence = []
	tok, pos, phrase_types = tokens_with_pos_and_phrase_types[i]
	sentence.append(' '.join([token, phrase_types, pos, entity]))
	i += 1
sentences.append(sentence)

full_length = len(sentences)
length_of_train_subset = int(args.train * full_length)
length_of_test_subset = int(args.test * full_length)

#random.shuffle(sentences)

write_sentences(sentences[:length_of_train_subset], TRAIN_FILE, preamble)
write_sentences(sentences[length_of_train_subset:length_of_train_subset + length_of_test_subset], TEST_FILE, preamble)
write_sentences(sentences[length_of_train_subset + length_of_test_subset:], DEV_FILE, preamble)
#print(len(sentences))
#print(sentences[-1])
#print(tokens_with_pos_and_phrase_types[i-1])
# Merge
#lines = list(map(lambda item: item[0], tokens_with_pos_and_phrase_types[:2]))
#for pair in zip(tokens_with_entities, tokens_with_pos_and_phrase_types[2:]):
#	if len(pair[1]) == 1:
#		lines.append('')
#	else:
#		lines.append(' '.join([pair[0][0], pair[1][2], pair[1][1], pair[0][1]]))
#write_lines(STANFORD_POS_FILE, lines)
#write_lines(STANFORD_POS_FILE, list([' '.join([pair[0][0], pair[1][2], pair[1][1], pair[0][1]]) for pair in zip(tokens_with_entities, tokens_with_pos_and_phrase_types)]))
#write_lines('stanford-ner-corpus-pos.txt', [' '.join(tokens),])