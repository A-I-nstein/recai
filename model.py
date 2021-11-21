import re
import nltk
import spacy
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def rem_spl_char(doc):
  return re.sub('[^A-Za-z0-9 ]+', '', doc)

def rem_stop_words(token_doc):
  return [w for w in token_doc if not w in stop_words]

def tokenize(doc):
  return word_tokenize(doc)

def lemma(tok_doc):
  sp = spacy.load('spacy_model')
  sentence = sp(" ".join(tok_doc))
  return [w.lemma_ for w in sentence]

def getStatsAndDocs(results):

  statutes_data = pd.read_csv('statutes.csv')
  caseDocs_data = pd.read_csv('caseDoc.csv')

  statutes = pd.read_csv('query_to_statutes.csv')
  caseDocs = pd.read_csv('query_to_case_document.csv')

  stat_file = {}
  doc_file = {}

  for aila_no in results:
    aila = 'AILA_Q' + str(int(aila_no[0]) + 1)

    summary_specific_stat = statutes[statutes['AILA'] == aila]
    for i in summary_specific_stat.columns:
      if(summary_specific_stat[i].item() == 1):
        data = statutes_data[i + '.txt']
        stat_file[data[0]] = data[1]

    summary_specific_docs = caseDocs[caseDocs['AILA'] == aila]
    count = 1
    for i in summary_specific_docs.columns:
      if(summary_specific_docs[i].item() == 1):
        key = 'Case Document ' + str(count)
        count += 1
        doc_file[key] = '\n\n'.join(caseDocs_data[i + '.txt'])

  return stat_file, doc_file

def predict(case_summary):
  model= Doc2Vec.load("d2v.model")
  query = lemma(rem_stop_words(tokenize(rem_spl_char(case_summary).lower())))
  result = model.docvecs.most_similar(positive=[model.infer_vector(query)],topn=2)
  statutes, case_docs = getStatsAndDocs(result)
  return (statutes, case_docs)
