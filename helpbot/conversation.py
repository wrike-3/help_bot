from joblib import load

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('stopwords')
nltk.download('wordnet')


class AnswerHandler:
    def __init__(self, config):
        self.vectorizer = load(config.vectorizer_path)
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = stopwords.words("english")
        self.model_chapter = load(config.model_chapter)
        self.model_section = load(config.model_section)
        self.model_paper = load(config.model_paper)
        self.encoder_chapter = load(config.encoder_chapter)
        self.encoder_section = load(config.encoder_section)
        self.encoder_paper = load(config.encoder_paper)

    def preprocess_text(self, text):
        tokens = self.tokenizer.tokenize(text)
        tokens = [token.lower() for token in tokens]
        tokens = [token for token in tokens if token not in self.stop_words \
                  and token != " "]
        lemmas = [self.lemmatizer.lemmatize(token) for token in tokens]
        clean_text = " ".join(lemmas)
        return clean_text

    def predict_text_classes(self, user_text):
        probable_classes = []
        clean_text = self.preprocess_text(user_text)
        x = [clean_text]
        vectorized = self.vectorizer.transform(x)
        encoders = [self.encoder_section, self.encoder_chapter, self.encoder_paper]
        models = [self.model_section, self.model_chapter, self.model_paper]
        for encoder, model in zip(encoders, models):
            prediction = model.predict_proba(vectorized)[0]
            categories = encoder.categories_[0]
            answer = sorted(zip(prediction, categories), reverse=True)[0]
            probable_classes.append(f'{answer[1]}: {answer[0]}')
        return '\n'.join(probable_classes)
