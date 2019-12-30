java -cp "/home/dima/CoreNLP/classes" edu.stanford.nlp.tagger.maxent.MaxentTagger -model /home/dima/models/russian-ud-pos.tagger -textFile text.txt -outputFormat tsv -outputFile pos.tag
java -cp "/home/dima/CoreNLP/target/classes" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos -keepPunct edu.stanford.nlp.trees.international.russian.RussianTreebankLanguagePack \
-embedFile /home/dima/models/ArModel100.txt \
-embeddingSize 100 \
-parse EnhancedDependenciesAnnotation \
-language Russian \
-textFile text.txt \
-outputFile pos-generalized-pipeline.txt \
-outputFormat conll \
-pos.model /home/dima/models/russian-ud-pos.tagger