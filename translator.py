from googletrans import Translator
from wonderwords import RandomWord
import textrazor
from config import textrazor_api_key


def translate(ru_word):
    """
    Перевод слова с русского на английский
    :param ru_word: Слово на русском языке
    :return: Слово на английском с заглавной буквы
    """
    translator = Translator()
    en_word = translator.translate(ru_word, src='ru', dest='en')
    return en_word.text.title()


def get_part_of_speech(en_word):
    """
    Получает тип слова (существительное, прилагательное, глагол)
    :param en_word: Слово на английском с заглавной буквы
    :return: тип слова (nouns, verbs, adjectives)
    """
    client = textrazor.TextRazor(api_key=textrazor_api_key, extractors=["words"])
    response = client.analyze(en_word)

    for sentence in response.sentences():
        part = sentence.words[0].part_of_speech
    match part:
        case 'NN' | 'NNS' | 'NNP' | 'NNPS':
            return 'nouns'
        case 'VB' | 'VBD' | 'VBG' | 'VBN' | 'VBP' | 'VBZ':
            return 'verbs'
        case 'JJ' | 'JJR' | 'JJS':
            return 'adjectives'
        case _:
            return None


def gen_wrong_answers(en_word):
    """
    Генерирует 3 случайных слова с тем же типом, как и исходное
    :param en_word: Слово на английском с заглавной буквы
    :return: Список из 3х английских слов с заглавной буквы
    """
    part = get_part_of_speech(en_word)
    word_generator = RandomWord()

    wrong_answers = []
    for ind in range(3):
        word = word_generator.word(include_parts_of_speech=[part])
        wrong_answers.append(word.title())

    return wrong_answers
