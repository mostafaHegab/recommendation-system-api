
from joblib import load 
loaded_joblib_model = load(filename="utils/Sentiment_Analysis_unigram.joblib")
feats = loaded_joblib_model.feature_names
feats_len = len(feats)

def sentiment_analyzer(sent):
    sent = sent.split(" ")
    sent_features=[]
    sent_dict = {}
    for word in sent:
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