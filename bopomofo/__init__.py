# -*- coding: utf-8 -*-
from .__version__ import __version__
from .dictionrary import pinyin_bopomofo as dict_pb
from xpinyin import Pinyin

# Create a 'xpinyin' instance
_pinyin = Pinyin()

class PinyinParsingError(Exception):
    pass


def to_bopomofo(chars, splitter=u' ', tones=True, first_tone_symbol=False):
    '''Translate words to bopomofo

    :param chars: The text string to be coverted
    :param splitter: The splitter between words
    :param first_tone_symbol: Display the first tone symbol or not.
        Default set to False
    '''

    return splitter.join(_bopomofo_list(chars, tones, first_tone_symbol))


def to_pinyin(chars, splitter=u' ', tones=False):
    '''Translate words to pinyin
    An API port of 'xpinyin.get_pinyin'
    '''

    return _pinyin.get_pinyin(chars, splitter, show_tone_marks=tones)


def _pinyin_list(chars, tones=False):
    '''Translate words to pinyin in list'''

    return _pinyin.get_pinyin(chars, '|', show_tone_marks=tones).split('|')


def _bopomofo_list(chars, tones=False, first_tone_symbol=False):
    '''Translate words to bopomofo in list'''

    pinyin = _pinyin_list(chars, tones)
    return [_single_pinyin_to_bopomofo(x, tones, first_tone_symbol, ignore_warning=True) for x in pinyin]


def _single_pinyin_to_bopomofo(pinyin, tones=False, first_tone_symbol=False, ignore_warning=False):
    '''Translate a single pinyin to bopomofo'''

    result = None
    raw = pinyin
    pinyin = pinyin.strip('! ').lower()
    normalized_pinyin, pinyin_tone = _single_pinyin_extarct_tone(pinyin)
    consonant = None
    vowel = None
    tone_symbol = ''

    if tones:
        # Skip if it's first tone, unless specified
        if pinyin_tone != 1 or first_tone_symbol:
            tone_symbol = dict_pb['tones']['bopomofo'][pinyin_tone]


    for con in dict_pb['special']:
        pin, bopo = con
        if normalized_pinyin == pin:
            return bopo + tone_symbol

    for con in dict_pb['consonants']:
        pin, bopo = con
        if normalized_pinyin.startswith(pin):
            result = bopo
            consonant = pin
            vowel = normalized_pinyin[len(pin):]
            break
    else:
        if (ignore_warning):
            return raw
        raise PinyinParsingError('Can not find consonant for pinyin "%s".' % pinyin)

    for vow in dict_pb['vowels']:
        pin, bopo = vow
        if vowel == pin:
            result += bopo
            break
    else:
        if (ignore_warning):
            return raw
        raise PinyinParsingError('Can not find vowel for pinyin "%s".' % pinyin)

    return result + tone_symbol

def _single_pinyin_extarct_tone(pinyin):
    tone = 0
    raw = pinyin
    pinyin = raw.strip().lower()
    normalized = raw
    for _tone, letters in dict_pb['tones']['pinyin'].items():
        # Ignore the zero-tone list
        if _tone == 0:
            continue
        for char_index, char in enumerate(letters):
            if char in pinyin:
                tone_char_index = pinyin.index(char)
                tone = _tone
                normalized = pinyin[:tone_char_index] \
                           + dict_pb['tones']['pinyin'][0][char_index] \
                           + pinyin[tone_char_index+1:]
                break
        else:
            continue
        break
    return normalized, tone
