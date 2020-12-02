from pymorphy2 import MorphAnalyzer   #  pip install pymorphy2
from num2words import num2words

morph = MorphAnalyzer()

HOURS_IN_TEXT = {
    "час":[1,21],
    "часов":[0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
    "часа":[2,3,4,22,23,24]
}
MINUTE = "минут"

MONTHS = [
 'январь',
 'февраль',
 'март',
 'апрель',
 'май',
 'июнь',
 'июль',
 'август',
 'сентябрь',
 'октябрь',
 'ноябрь',
 'декабрь'
]

def get_minute_str(minute:int):
    str_minute = num2words(minute,lang="ru",to="cardinal")
    ending = morph.parse(MINUTE)[0]
    buf = str.split(str_minute, ' ')
    #
    end_word_minute = morph.parse(buf[-1])[0]
    #end_word_minute = end_word_minute.inflect({'femn'})
    if end_word_minute.tag.number:
        ending = ending.inflect({'gent'})

    if end_word_minute:
        if len(buf) > 1:
            str_minute = buf[0] + " " + end_word_minute.word
        else:
            str_minute = end_word_minute.word

    return str_minute + " " + ending.word

def get_hour_str(hour:int):
    str_hours = num2words(hour, lang="ru")
    ending = ""
    for key, value in HOURS_IN_TEXT.items():
        if hour in value:
            ending = key
            break
    return str_hours + " " + ending

def get_month_num(month):
    mapping = {mon:n for n, mon in enumerate(MONTHS, 1)}
    month_norm = morph.parse(month)[0].normal_form
    return mapping.get(month_norm)

def get_month_name(month):
    if isinstance(month, int) and 1 <= month <= 12:
        return MONTHS[month-1]
    return None

def get_month_soon(month):
    if isinstance(month, int) and 1 <= month <= 12:
        month = MONTHS[month-1]
    p = morph.parse(month)[0]
    if p:
        loct = p.inflect({"loct"})
    if loct and p.normal_form in MONTHS:
        return f"в {loct[0]}"
    return None

def get_month_gen(month):
    if isinstance(month, int) and 1 <= month <= 12:
        month = MONTHS[month-1]
    p = morph.parse(month)[0]
    if p:
        gent = p.inflect({"gent"})
    if gent and p.normal_form in MONTHS:
        return gent[0]
    return None



def plural_days(n):
    days = ['день', 'дня', 'дней']

    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return days[p]