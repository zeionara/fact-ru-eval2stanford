from convert import read_lines, write_lines
import argparse, random, re, os

structure_stanford_deps = __import__('structure-stanford-deps')

random.seed(171)


TRAIN_FILE = 'conll2003ru/train.txt'
TEST_FILE = 'conll2003ru/test.txt'
DEV_FILE = 'conll2003ru/dev.txt'

STANFORD_POS_FILE = 'ru-conll2003.txt'
STANFORD_FILE = 'stanford-ner-corpus.txt'
POS_FILE = 'phrase_types.txt'

NO_ENTITY_MARK = 'O'

MERGEABLE_STANFORD_TOKEN_PAIRS = [[re.compile('^-$'), re.compile('[а-яА-ЯёЁ]+')]]

CV_ROOT = 'conll2003rucv'

ignored_sequences = ['—', "«", '»', '"', '(', ')', '…', '–']

TAG_MAPPING = {'B-Facility': 'B-Org', 'B-Project': 'B-Org', 'I-Project': 'I-Org', 'I-Facility': 'I-Org'}

MAX_DISTANCE_BETWEEN_MATCHING_TOKENS = 12

# Add bio prefixes for entities labels
def add_bio_prefixes(tokens_with_entities):
    previous_entity = ''
    new_tokens_with_entities = []
    for token, entity in tokens_with_entities:
        new_tokens_with_entities.append((token, f'{structure_stanford_deps.get_bio_prefix(previous_entity, entity) if entity != NO_ENTITY_MARK else ""}{entity}'))
        previous_entity = entity
    return new_tokens_with_entities

def flatten_sentences(sentences):
    flattened = []
    for sentence in sentences:
        for line in sentence:
            flattened.append(line)
        flattened.append('')
    return flattened

def write_sentences(sentences, filename, preamble):
    write_lines(filename, preamble + flatten_sentences(sentences))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--train', type=float, default=0.7)
    parser.add_argument('--test', type=float, default=0.2)
    parser.add_argument("--cv", action="store_true")

    args = parser.parse_args()

    # Source file
    tokens_with_entities = add_bio_prefixes([line.split(' ') for line in read_lines(STANFORD_FILE)])
    # Stanford output
    tokens_with_pos_and_phrase_types = [line.split(' ') for line in read_lines(POS_FILE)[:]]
    
    # Merge two files
    preamble = list(map(lambda item: ' '.join(item), tokens_with_pos_and_phrase_types[:2]))
    sentences = []
    sentence = []
    i = 2
    mismatching_tokens_counter = 0
    max_number_of_mismatching_tokens = 100
    skip_iterations = 0
    for j in range(len(tokens_with_entities)):
        if skip_iterations > 0:
            skip_iterations -= 1
            continue
        # Skip repeating lines in the source file
        if j > 0 and tokens_with_entities[j - 1] == tokens_with_entities[j]:
            continue

        # Get token enad entity from the source data
        token, entity = tokens_with_entities[j]
        
        if i >= len(tokens_with_pos_and_phrase_types):
            break
        
        # Delete exactly one empty line
        were_deleted_empty_lines = False
        while len(tokens_with_pos_and_phrase_types[i]) == 1:
            i += 1
            if not were_deleted_empty_lines:
                were_deleted_empty_lines = True
        
        # If deleted empty line then finish collected sentence
        if were_deleted_empty_lines:
            sentences.append(sentence)
            sentence = []

        # Try to skip tokens in stanford results
        for k in range(MAX_DISTANCE_BETWEEN_MATCHING_TOKENS):
            if i < len(tokens_with_pos_and_phrase_types) - k and token != tokens_with_pos_and_phrase_types[i][0] and token == tokens_with_pos_and_phrase_types[i + k][0]:
                #print(f'{j} skipped {tokens_with_entities[j + 1][0]} = {tok}')
                i += k
        
        # Get token and associated data from the stanford output
        tok, pos, phrase_types = tokens_with_pos_and_phrase_types[i]
        next_tok = None if i + 1 == len(tokens_with_pos_and_phrase_types) else tokens_with_pos_and_phrase_types[i + 1][0]

        # Try to skip tokens in the source file
        for k in range(MAX_DISTANCE_BETWEEN_MATCHING_TOKENS):
            if j < len(tokens_with_entities) - k and token != tok and tokens_with_entities[j + k][0] == tok:
                #print(f'{j} skipped {tokens_with_entities[j + 1][0]} = {tok}')
                skip_iterations = k
                break

        if (skip_iterations > 0):
            skip_iterations -= 1
            continue

        # Merge tokens incorrectly splitted by stanford
        for mergeable_pair_pattern in MERGEABLE_STANFORD_TOKEN_PAIRS:
            if mergeable_pair_pattern[0].match(tok) and mergeable_pair_pattern[1].match(next_tok) and f'{tok}{next_tok}' == token:
                #print(f'Merging tokens {tok} and {next_tok}')
                tok = f'{tok}{next_tok}'
                i += 1

        # Append token to the current sentence
        if token != tok and token not in ignored_sequences: #and mismatching_tokens_counter <= max_number_of_mismatching_tokens and token not in ignored_sequences:
            print(i, token, entity, tok)
            mismatching_tokens_counter += 1

        sentence.append(' '.join([token, phrase_types, pos, TAG_MAPPING.get(entity, entity)]))
        i += 1

    # Append the last sentence if it is not empty
    if len(sentence) > 0:
        sentences.append(sentence)

    full_length = len(sentences)
    length_of_train_subset = int(args.train * full_length)
    length_of_test_subset = int(args.test * full_length)

    random.shuffle(sentences)

    if not args.cv:
        write_sentences(sentences[:length_of_train_subset], TRAIN_FILE, preamble)
        write_sentences(sentences[length_of_train_subset:length_of_train_subset + length_of_test_subset], TEST_FILE, preamble)
        write_sentences(sentences[length_of_train_subset + length_of_test_subset:], DEV_FILE, preamble)
    else:
        if not os.path.isdir(CV_ROOT):
            os.mkdir(CV_ROOT)
        for i in range(int(1.0/(1-args.train))):
            subset_root = f'{CV_ROOT}/{i + 1:02d}'
            length_of_test_subset = int((1 - args.train) * full_length)
            if not os.path.isdir(subset_root):
                os.mkdir(subset_root)
            test_sentences = sentences[i*length_of_test_subset:min((i+1)*length_of_test_subset, full_length)]
            train_sentences = sentences[0:i*length_of_test_subset] + sentences[min((i+1)*length_of_test_subset, full_length):full_length]

            print(f'Cv subset {i:02d} contains {len(train_sentences)} train and {len(test_sentences)} test_sentences')

            write_sentences(test_sentences, f'{subset_root}/{TEST_FILE.split("/")[1]}', preamble)
            write_sentences(train_sentences, f'{subset_root}/{TRAIN_FILE.split("/")[1]}', preamble)