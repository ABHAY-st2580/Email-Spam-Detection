import streamlit as st
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from nltk.stem.porter import PorterStemmer


def transform_text(text):
    text = text.lower()
    text = word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    ps = PorterStemmer()
    for i in text:
        y.append(ps.stem(i))
    text = y[:]
    y.clear()
    return " ".join(text)


tfidf = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))


st.title("EMAIL/SMS SPAM DETECTION")

input_mssg = st.text_area("Enter the Message")

if st.button("Predict"):
    transformed_mssg = transform_text(input_mssg)
    vector_input = tfidf.transform([transformed_mssg])

    result = model.predict(vector_input)[0]

    if result == 0:
        st.header("Legitimate")
    else:
        st.header("Spam/Phishing")



