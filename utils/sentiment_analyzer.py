from joblib import load
import string
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import datetime
import re
import string
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import wordnet
from nltk import ngrams
# The following code creates a word-document matrix.
from sklearn.feature_extraction.text import CountVectorizer
#Installing emot library
from emot.emo_unicode import UNICODE_EMO, EMOTICONS
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

loaded_joblib_model = load(filename="Sentiment_Analysis_unigram.joblib")
feats = loaded_joblib_model.feature_names
feats_len = len(feats)
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def sentiment_analyzer(text):
    def convert_emoticons(text):
         for emot in EMOTICONS:
             text = re.sub(u'('+emot+')', " ".join(EMOTICONS[emot].replace(",","").split()), text)
         return text
    convert_emoticon1=convert_emoticons(text)

    # Function for converting emojis into word
    def convert_emojis(text):
        for emot in UNICODE_EMO:
            text = text.replace(emot, "_".join(UNICODE_EMO[emot].replace(",","").replace(":","").split()))
        return text
    text1 = convert_emoticon1
    text2 =convert_emojis(text1)
    from spellchecker import SpellChecker
    text=text2
    spell = SpellChecker()
    def correct_spellings(text):
        corrected_text = []
        misspelled_words = spell.unknown(text.split())
        for word in text.split():
            if word in misspelled_words:
                corrected_text.append(spell.correction(word))
            else:
                corrected_text.append(word)
        return " ".join(corrected_text)
    sent1 =correct_spellings(text)
    sent =sent1
    sent =sent.lower()
    sent = sent.translate(str.maketrans('', '', string.punctuation))
    filtered_sentence = [] 
    stop_words = set(stopwords.words('english')) 
    stop_words.remove('not')
    word_tokens =word_tokenize(sent)
    filtered_sentence = [w for w in word_tokens if not w in stop_words ]
    listToStr = ' '.join(map(str, filtered_sentence))
    lemmatizer = WordNetLemmatizer()
    wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}
    def lemmatize_words(text):
        pos_tagged_text = nltk.pos_tag(word_tokenize(text))
        return ([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text])
    lemmatized_output =[]
    lemmatized_output = lemmatize_words(listToStr)

    sent_features=[]
    sent_dict = {}
    for word in lemmatized_output:
      if not word in sent_dict:
        sent_dict[word] = 0
      sent_dict[word] = sent_dict[word] + 1
    for i in range(feats_len):
     if not feats[i] in sent_dict:
       sent_features.append(0)
     else:
       sent_features.append(sent_dict[feats[i]])
    joblib_y_preds = loaded_joblib_model.predict([sent_features])
    return joblib_y_preds[0]
