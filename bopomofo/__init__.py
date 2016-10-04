# -*- coding: utf-8 -*-

from xpinyin import Pinyin
from .dictionrary import pinyin_bopomofo as dict_pb

# Create a 'xpinyin' instance
_pinyin = Pinyin()

class PinyinParsingError(Exception):
    pass

# Export the api of 'xpinyin'
to_pinyin = _pinyin.get_pinyin


def to_bopomofo(chars, splitter=u'、', tones=True):
    '''Translate words to bopomofo'''

    return splitter.join(_bopomofo_list(chars, show_tone_marks))


def _pinyin_list(chars, tone=False):
    '''Translate words to pinyin in list'''

    return _pinyin.get_pinyin(chars, '|').split('|')


def _bopomofo_list(chars, tone=False):
    '''Translate words to bopomofo in list'''

    pinyin = _pinyin_list(chars, tone)
    return [_single_pinyin_to_bopomofo(x, tone) for x in pinyin]


def _single_pinyin_to_bopomofo(pinyin, tone=False, ignore_warning=False):
    '''Translate a single pinyin to bopomofo'''

    result = None
    pinyin = pinyin.strip().lower()
    consonant = None
    vowel = None

    for con in dict_pb['special']:
        pin, bopo = con
        if pinyin == pin:
            return bopo

    for con in dict_pb['consonants']:
        pin, bopo = con
        if pinyin.startswith(pin):
            result = bopo
            consonant = pin
            vowel = pinyin[len(pin):]
            break
    else:
        if (ignore_warning):
            return ''
        raise PinyinParsingError('Can not find consonant for pinyin "%s".' % pinyin)

    for vow in dict_pb['vowels']:
        pin, bopo = vow
        if vowel == pin:
            result += bopo
            break
    else:
        if (ignore_warning):
            return ''
        raise PinyinParsingError('Can not find vowel for pinyin "%s".' % pinyin)

    return result
