# Usage
## Convert fact ru eval data to stanford format
```sh
python3 convert.py /home/dima/factRuEval-2016/devset/
```  
Result will be stored in the file `stanford-ner-corpus.txt` in the following format:
```
Правительство Org
Японии Org
выразило O
решительный O
протест O
против O
состоявшегося O
в O
пятницу O
визита O
российского O
министра O
обороны O
, O
посетившего O
южные Location
Курильские Location
острова Location
```
## Add POS tags
### Prerequisites
1. Stanford CoreNLP
2. POS tagger model
### Perform tagging
```sh
java -cp "/home/dima/CoreNLP/target/classes" edu.stanford.nlp.tagger.maxent.MaxentTagger -model /home/dima/models/russian-ud-pos.tagger -textFile text.txt -outputFormat tsv -outputFile pos.tag
``` 
As a result you'll have got a 'pos.tag' file in the following format:  
```
Правительство	NOUN
Японии	PROPN
выразило	VERB
решительный	ADJ
протест	NOUN
против	ADP
состоявшегося	VERB
в	ADP
пятницу	NOUN
визита	NOUN
российского	ADJ
министра	NOUN
обороны	NOUN
,	PUNCT
посетившего	VERB
южные	ADJ
Курильские	ADJ
острова	NOUN
```
### Merge POS tags with entities
```sh
python3 merge-pos-with-entities.py
```
As a result you'll have got a joined file `stanford-ner-corpus-pos.txt` with both - POS tags and entity tags in the following format:  
```
Правительство NOUN Org
Японии PROPN Org
выразило VERB O
решительный ADJ O
протест NOUN O
против ADP O
состоявшегося VERB O
в ADP O
пятницу NOUN O
визита NOUN O
российского ADJ O
министра NOUN O
обороны NOUN O
, PUNCT O
посетившего VERB O
южные ADJ Location
Курильские ADJ Location
острова NOUN Location
```
## Add constituency
### Prerequisites
1. Stanford CoreNLP + dependency tagging model
2. POS tagger model
3. Embeddings model used when training dependency tagging model
### Perform tagging
```sh
java -cp "/home/dima/CoreNLP/target/classes" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,depparse -keepPunct edu.stanford.nlp.trees.international.russian.RussianTreebankLanguagePack \
-embedFile /home/dima/models/ArModel100.txt \
-embeddingSize 100 \
-parse EnhancedDependenciesAnnotation \
-depparse.model /home/dima/models/nndep.rus.modelAr100HS400.txt.gz \
-language Russian \
-textFile text.txt \
-outFile dep-puncts.txt \
-pos.model /home/dima/models/russian-ud-pos.tagger
```
### Structure results from Stanford
```sh
python3 structure-stanford-deps.py
```  
This will output dependency tree for each sentence in the following format to the file `dependency_trees.txt`:  
```
("ROOT"/"ROOT"/0
  ("выразило"/"VERB"/3
    ("Правительство"/"NOUN"/1
      ("Японии"/"PROPN"/2)
    )
    ("протест"/"NOUN"/5
      ("решительный"/"ADJ"/4)
      ("визита"/"NOUN"/10
        ("против"/"ADP"/6)
        ("состоявшегося"/"VERB"/7
          ("пятницу"/"NOUN"/9
            ("в"/"ADP"/8)
          )
        )
        ("министра"/"NOUN"/12
          ("российского"/"ADJ"/11)
          ("обороны"/"NOUN"/13)
        )
      )
    )
    (","/"PUNCT"/14)
    ("посетившего"/"VERB"/15
      ("острова"/"NOUN"/18
        ("южные"/"ADJ"/16)
        ("Курильские"/"ADJ"/17)
        ("считают"/"VERB"/26
          (","/"PUNCT"/19)
          ("которые"/"PRON"/20
            ("Япония"/"PROPN"/22
              ("и"/"PART"/21)
            )
            (","/"PUNCT"/23)
            ("Россия"/"PROPN"/25
              ("и"/"CCONJ"/24)
            )
          )
          ("своими"/"DET"/27)
        )
      )
    )
    ("."/"PUNCT"/28)
  )
)

```
### Translate dependency tree into consistency structure
TODO: Encountered problem with different tokenization and consequent alignment errors in `facts-ru-eval` and `stanford corenlp`.