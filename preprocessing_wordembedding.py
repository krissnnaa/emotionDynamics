from gensim.models import Word2Vec
import nltk

mysentence="I am a student."
token_words=nltk.tokenize.word_tokenize(mysentence)
model=Word2Vec([token_words],window=2,size=10, min_count=1)
print(model.wv.vocab)
print(model.wv.vectors)
model.wv.save_word2vec_format('model.txt', binary=False)