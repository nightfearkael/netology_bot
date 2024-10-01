from pg_connector import Postgre

pg_conn = Postgre()

word_list = [['Кошка', 'Cat', 'Dog, Turtle, Pigeon'],
['Собака', 'Dog', 'Whale, Mouse, Hat'],
['Самолет', 'Airplane', 'Train, Car, House'],
['Дом', 'House', 'Cart, Pitch, Roof'],
['Мышь', 'Mouse', 'Hamster, Cat, Dog'],
['Игрок', 'Player', 'Spotter, Stealer, Robber'],
['Музыкант', 'Artist', 'Star, Player, Chair'],
['Телефон', 'Phone', 'Mail, Can, Stairs'],
['Письмо', 'Mail', 'Plubmer, Paper, Cross'],
['Ошибка', 'Error', 'True, Start, Exception']]


for word in word_list:
    ru_word = word[0]
    en_word = word[1]
    answers = word[2]
    choices = answers.split(',')[:3]
    choices.append(en_word)
    pg_conn.add_word(ru_word, en_word)
    word_id = pg_conn.find_word_id(ru_word)
    pg_conn.add_choices(word_id[0], choices)
