from bottle import*
from random import choice
import random
import datetime
from datetime import date
import string

horoscope = {}


@route('/forer')
@view('html_marking')
def for_sign():

    fate = choice(("хорошо", "плохо"))
    #return dict(sign=html_marking,dest = fate)


def getTextFromHoroscope(sign):
    d = date.today()
    if (d, sign) not in horoscope:
        horoscope[(d, sign)] = gen_horoscope()

    return horoscope[(d, sign)]


def show_time():
    now = datetime.datetime.now()
    now = now.strftime('%a. %d %b %Y')
    return now


def prepare_horoscope():
    with open('text.txt', encoding='utf-8') as f:
        global words
        words = []
        words = f.read().split()
    markov_chain = {}
    for i in range(0, len(words) - 2):
        key = (words[i], words[i+1])
        markov_chain.setdefault(key, [])
        markov_chain[key].append(words[i+2])
    return markov_chain


def gen_horoscope():
    stopsentence = (".", "!", "?",)
    markov_chain = prepare_horoscope()
    size = 25
    gen_words = []
    seed = random.randint(0, len(words) - 3)
    w1 = words[seed]
    while (w1.isupper()  or w1.islower()):
        seed = random.randint(0, len(words) - 3)
        w1 = words[seed]
    w2 = words[seed+1]

    for i in range(0, size-1):
        gen_words.append(w1)
        try:
            w3 = choice(markov_chain[(w1,w2)])
        except KeyError:
            break
        w1, w2 = w2, w3

    while True:
        gen_words.append(w1)
        if w1[-1] in stopsentence:
             break
        try:
            w3 = choice(markov_chain[(w1,w2)])
        except KeyError:
            break
        w1, w2 = w2, w3
    result = ' '.join(gen_words)
    return result


def sign_period(ast_sign):
    periods = {'Овен': '20 марта — 19 апреля','Телец': '20 апреля — 20 мая', 'Близнецы':
'21 мая — 20 июня','Рак':
'21 июня — 22 июля', 'Лев':
'23 июля — 22 августа', 'Дева':
'23 августа — 22 сентября', 'Весы':
'23 сентября — 22 октября', 'Скорпион':
'23 октября — 21 ноября', 'Стрелец':
'22 ноября — 21 декабря', 'Козерог':
'22 декабря — 19 января', 'Водолей':
'21 января — 18 февраля', 'Рыбы':
'19 февраля — 19 марта'}

    get_period = periods[ast_sign]
    return get_period


@route('/forer/<ast_sign>')
@view('ast_sign')
def get_page(ast_sign):
    h = getTextFromHoroscope(ast_sign)
    t = show_time()
    this_period = sign_period(ast_sign)
    return dict(sign = ast_sign, h = h, t = t, this_period = this_period)


run(host='localhost', port=8080, debug=True)

