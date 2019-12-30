java -cp "/home/dima/CoreNLP/target/classes" edu.stanford.nlp.parser.nndep.DependencyParser edu.stanford.nlp.trees.international.russian.RussianTreebankLanguagePack \
-embedFile /home/dima/models/ArModel100.txt \
-embeddingSize 100 \
-model /home/dima/models/nndep.rus.modelAr100HS400.txt.gz \
-language Russian \
-textFile text.txt \
-outFile dep.txt \
-tagger.model /home/dima/models/russian-ud-pos.tagger
java -cp "/home/dima/CoreNLP/target/classes" edu.stanford.nlp.parser.nndep.DependencyParser -keepPunct edu.stanford.nlp.trees.international.russian.RussianTreebankLanguagePack \
-embedFile /home/dima/models/ArModel100.txt \
-outputFormat "wordsAndTags" \
-embeddingSize 100 \
-parse EnhancedDependenciesAnnotation \
-model /home/dima/models/nndep.rus.modelAr100HS400.txt.gz \
-language Russian \
-textFile text.txt \
-outFile dep-puncts.txt \
-tagger.model /home/dima/models/russian-ud-pos.tagger
java -cp "/home/dima/CoreNLP/target/classes" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,depparse -keepPunct edu.stanford.nlp.trees.international.russian.RussianTreebankLanguagePack \
-embedFile /home/dima/models/ArModel100.txt \
-embeddingSize 100 \
-tokenize.whitespace True \
-parse EnhancedDependenciesAnnotation \
-depparse.model /home/dima/models/nndep.rus.modelAr100HS400.txt.gz \
-language Russian \
-textFile text.txt \
-output dep-puncts.txt \
-pos.model /home/dima/models/russian-ud-pos.tagger
