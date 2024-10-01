from googletrans import Translator


def translate(ru_word):
    """
    Перевод слова с русского на английский
    :param ru_word: Слово на русском языке
    :return: Слово на английском с заглавной буквы
    """
    translator = Translator()
    en_word = translator.translate(ru_word, src='ru', dest='en')
    return en_word.text.title()




