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
### Perform tagging [deprecated - feel free to proceed to the next stage if you are not interested in extracting entities separately from dependencies]
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
### Merge POS tags with entities [deprecated - feel free to proceed to the next stage if you are not interested in extracting entities separately from dependencies]
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
And constituency structures along with `POS` tags to file `phrase-types.txt`.  
You need to manually find and delete repeatings using regexp `^(.*)(\r?\n\1)+$`.
### Merge POS tags and Constituency info with entities
```sh
python3 merge-pos-and-constituency-with-entities.py
```
To merge and split into test, dev and train at once:
```sh
python3 merge.py --train 0.7 --test 0.15
```
As a result you'll have got a joined file `stanford-ner-corpus-pos.txt` with both - POS tags and entity tags in the following format:  
```
равительство NOUN NP Org
Японии PROPN NP Org
выразило VERB VP O
решительный ADJ NP O
протест NOUN NP O
против ADP NP O
состоявшегося VERB VP O
в ADP NP O
пятницу NOUN NP O
визита NOUN NP O
российского ADJ NP O
министра NOUN NP O
обороны NOUN NP O
, PUNCT VP O
посетившего VERB VP O
южные ADJ NP Location
Курильские ADJ NP Location
острова NOUN NP Location
, PUNCT VP O
которые PRON VP O
и PART VP O
Япония PROPN VP LocOrg
, PUNCT VP O
и CCONJ VP O
Россия PROPN VP LocOrg
```  
which can be used in transformers-ner.