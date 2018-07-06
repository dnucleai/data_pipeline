from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

'''
Helper class to clean text through removing invalid characters,
removing stop words such as the, a, an, and etc., and normalizing
words through using a WordNetLemmatizer.
'''


class Cleaner:
    STOP_WORDS = set(stopwords.words('english'))
    CHARACTERS_TO_EXCLUDE = set(string.punctuation)
    LEMMA = WordNetLemmatizer()
    INDEX_FORBIDDEN_CHARS = [" ", "\"", "*", "\\", "<", "|", ",", ">", "/", "?"]

    def __init__(self):
        pass

    @staticmethod
    def format_es_fields(text):
        for forbidden in Cleaner.INDEX_FORBIDDEN_CHARS:
            text = text.lower().replace(forbidden, "_")
        return text

    @staticmethod
    def clean(text):
        ascii_text = Cleaner.__remove_non_ascii_chars(text)
        ascii_no_stop_words_text = Cleaner.__remove_stop_words(ascii_text)
        return Cleaner.__normalize_words(ascii_no_stop_words_text)

    @staticmethod
    def __remove_non_ascii_chars(words):
        return ''.join([c if ord(c) < 128 else ' ' for c in words])

    @staticmethod
    def __remove_stop_words(words):
        return ' '.join([word for word in words.split() if word.lower() not in Cleaner.STOP_WORDS])

    @staticmethod
    def __normalize_words(words):
        return " ".join(Cleaner.LEMMA.lemmatize(word) for word in words.split())
