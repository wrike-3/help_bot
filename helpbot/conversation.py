from joblib import load
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
import pandas as pd

nltk.download('stopwords')
nltk.download('wordnet')


class AnswerHandler:
    def __init__(self, config):
        self.vectorizer = load(config.vectorizer)
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = stopwords.words("english")
        self.section_1_encoder = load(config.section_1_encoder)
        self.section_2_encoder = load(config.section_2_encoder)
        self.section_3_encoder = load(config.section_3_encoder)
        self.section_1_ovr = load(config.section_1_ovr)
        self.section_2_ovr = load(config.section_2_ovr)
        self.section_3_ovr = load(config.section_3_ovr)
        self.data = pd.read_csv(config.data)

    def preprocess_text(self, text):
        tokens = self.tokenizer.tokenize(text)
        tokens = [token.lower() for token in tokens]
        tokens = [token for token in tokens if token not in self.stop_words \
                  and token != " "]
        lemmas = [self.lemmatizer.lemmatize(token) for token in tokens]
        clean_text = " ".join(lemmas)
        return clean_text

    def predict_text_classes(self, user_text):
        probable_classes = {}
        clean_text = self.preprocess_text(user_text)
        x = [clean_text]
        vectorized = self.vectorizer.transform(x)
        sections = ['section_1', 'section_2', 'section_3']
        encoders = [self.section_1_encoder, self.section_2_encoder, self.section_3_encoder]
        models = [self.section_1_ovr, self.section_2_ovr, self.section_3_ovr]
        for encoder, model, section in zip(encoders, models, sections):
            prediction = model.predict_proba(vectorized)[0]
            categories = encoder.categories_[0]
            answer = sorted(zip(prediction, categories), reverse=True)[0]
            probable_classes[section] = answer[1]
        return probable_classes

    def return_answer(self, user_text):
        probable_classes = self.predict_text_classes(user_text)
        if len(self.data[(self.data.section_1 == probable_classes['section_1']) &
                         (self.data.section_2 == probable_classes['section_2']) &
                         (self.data.section_3 == probable_classes['section_3'])]) == 0:
            if len(self.data[(self.data.section_1 == probable_classes['section_1']) &
                             (self.data.section_2 == probable_classes['section_2'])]) == 0:
                sections_to_test = self.data[(self.data.section_1 == probable_classes['section_1'])]
            else:
                sections_to_test = self.data[(self.data.section_1 == probable_classes['section_1']) &
                                             (self.data.section_2 == probable_classes['section_2'])]
        else:
            sections_to_test = self.data[(self.data.section_1 == probable_classes['section_1']) &
                                         (self.data.section_2 == probable_classes['section_2']) &
                                         (self.data.section_3 == probable_classes['section_3'])]
        finish_answers = []
        for i, row in sections_to_test.iterrows():
            section_text = self.preprocess_text(row['section_text'])
            vectorized_section = self.vectorizer.transform([section_text])
            user_cleaned = self.preprocess_text(user_text)
            vectorized_user = self.vectorizer.transform([user_cleaned])
            answer = (cosine_similarity(vectorized_section, vectorized_user)[0][0],
                      row['section_text'], row['url_4'])
            finish_answers.append(answer)
        finish_answers.sort(key=lambda tup: tup[0], reverse=True)
        # best_section = finish_answers[0]
        answer_text = '\n'.join([f'{best_section[1]}. URL: {best_section[2]}' for best_section in finish_answers[:3]])
        return answer_text
