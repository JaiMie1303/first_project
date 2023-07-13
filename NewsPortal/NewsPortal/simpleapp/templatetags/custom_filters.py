from django import template

register = template.Library()

CENS = ['редиска', 'крендель', 'мякиш']


@register.filter()
def censor(text):
    text_censor = ''
    text = text.lower()
    for word in text.split():
        if word.strip('.,"/') in CENS:
            word = word[:1] + '*' * (len(word[1:]))
        text_censor += f' {word}'
    return text_censor