import sys, os

FACT_RU_EVAL_FOLDER = sys.argv[-1] if len(sys.argv) > 1 else 'data/fact-ru-eval/'
STANFORD_FILE = 'stanford-ner-corpus.txt'
NOT_ENTITY_MARK = 'O'

def read_lines(filename):
	with open(filename) as f:
		return [line.replace('\n', '') for line in f.readlines()]

def write_lines(filename, lines):
	with open(filename, "w") as f:
		f.write('\n'.join(lines))

if __name__ == "__main__":
	# Get unique input file names without extensions
	input_files = set()
	for r, d, f in os.walk(FACT_RU_EVAL_FOLDER):
	    for file in f:
	        input_files.add(file.split('.')[0])

	lines = []
	for input_file_name in input_files:
		# Doesn't support nested or overlapping entities
		spans = {}
		for line in read_lines(f'{FACT_RU_EVAL_FOLDER}{input_file_name}.spans'):
			splitted_line = line.split(' ')
			if len(splitted_line) > 1:
				spans[int(splitted_line[0])] = int(splitted_line[4])
		objects = {}
		for line in read_lines(f'{FACT_RU_EVAL_FOLDER}{input_file_name}.objects'):
			splitted_line = line.split(' ')
			for key in list(map(lambda id: int(id), splitted_line[2:splitted_line.index('#')])):
				objects[spans.get(key)] = splitted_line[1]
		for line in read_lines(f'{FACT_RU_EVAL_FOLDER}{input_file_name}.tokens'):
			splitted_line = line.split(' ')
			if len(splitted_line) > 1:
				lines.append(f'{splitted_line[3]} {objects.get(int(splitted_line[0]), NOT_ENTITY_MARK)}')

	write_lines(STANFORD_FILE, lines)