from sklearn.linear_model import SGDRegressor
from nltk.stem.snowball import EnglishStemmer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


def normalize(text):
    stemmer = EnglishStemmer()
    return ' '.join([stemmer.stem(s) for s in text.split()])


def predict_articles(reader, articles, n=5):
    from reader.documents import ReadRecord
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDRegressor())])
    records = ReadRecord.objects(reader=reader)
    text_clf.fit([normalize(x.article.content_text) for x in records],
                 [(1 if x.is_liked else 0) for x in records])
    predicted = text_clf.predict([normalize(x.content_text) for x in articles])
    return sorted(zip(list(articles), list(predicted)),
                  key=lambda t: t[1],
                  reverse=True)[:n]
