# -*- coding: utf-8 -*-
import sys
import re
from xpinyin import Pinyin

from .__version__ import __version__
from .dictionrary import pinyin_bopomofo as _dict

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

    return _pinyin.get_pinyin(chars, splitter, tone_marks=tones)

def bopomofo_to_pinyin(bopomofo, splitter=u' ', tones=True, default_tone=1):
    '''Translate bopomofo to pinyin'''

    bopomofos = _bopomofo_split(bopomofo, splitter)
    return splitter.join([_single_bopomofo_to_pinyin(x, tones, default_tone, ignore_warning=True) for x in bopomofos])


def _bopomofo_split(bopomofo, splitter=u' '):
    tones = u''.join(_dict['tones']['bopomofo'].values()) + splitter
    vacabulary = _dict['vacabulary'] + tones
    bopomofos = []
    pre_index = 0
    not_bopomofo = False
    for index, char in enumerate(bopomofo):
        if char not in vacabulary:
            not_bopomofo = True
        else:
            if not_bopomofo:
                bopomofos.append(bopomofo[pre_index:index])
                pre_index = index
            not_bopomofo = False
            if char in tones:
                bopomofos.append(bopomofo[pre_index:index+1])
                pre_index = index + 1
    return bopomofos

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
            tone_symbol = _dict['tones']['bopomofo'][pinyin_tone]


    for con in _dict['special']:
        pin, bopo = con
        if normalized_pinyin == pin:
            return bopo + tone_symbol

    for con in _dict['consonants']:
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

    for vow in _dict['vowels']:
        pin, bopo = vow
        if vowel == pin:
            result += bopo
            break
    else:
        if (ignore_warning):
            return raw
        raise PinyinParsingError('Can not find vowel for pinyin "%s".' % pinyin)

    return result + tone_symbol


def _single_bopomofo_to_pinyin(bopomofo, tones=False, default_tone=1, ignore_warning=False):
    result = None
    raw = bopomofo
    tone_index = default_tone
    normalized = raw.strip()
    for index, tone_symbol in _dict['tones']['bopomofo'].items():
        if normalized.endswith(tone_symbol):
            tone_index = index
            normalized = normalized.rstrip(tone_symbol)

    if not tones:
        tone_index = 0

    for pin, bopo in _dict['special']:
        if normalized == bopo:
            return _single_pinyin_append_tone(pin, tone_index)

    for pin, bopo in _dict['consonants']:
        if normalized.startswith(bopo):
            result = pin
            consonant = bopo
            vowel = normalized[len(bopo):]
            break
    else:
        if (ignore_warning):
            return raw
        raise PinyinParsingError('Can not find consonant for bopomofo "%s".' % bopomofo)

    for pin, bopo in _dict['vowels']:
        if vowel == bopo:
            result += pin
            break
    else:
        if (ignore_warning): # pragma: no cover
            return raw
        raise PinyinParsingError('Can not find consonant for bopomofo "%s".' % bopomofo)

    return _single_pinyin_append_tone(result, tone_index)


def _single_pinyin_append_tone(pinyin, tone):
    t = pinyin
    if tone != 0:
        m = re.search(u"[aoeiuv\u00fc]+", t)
        if m is None: # pragma: no cover
            pass
        elif len(m.group(0)) == 1:
            # if just find one vowels, put the mark on it
            t = t[:m.start(0)] \
                + _dict['tones']['pinyin'][tone][_dict['tones']['pinyin'][0].index(m.group(0))] \
                + t[m.end(0):]
        else:
            # mark on vowels which search with "a, o, e" one by one
            # when "i" and "u" stand together, make the vowels behind
            for num, vowels in enumerate((u"a", u"o", u"e", u"ui", u"iu")):
                if vowels in t:
                    t = t.replace(vowels[-1], _dict['tones']['pinyin'][tone][num])
                    break
    return t


def _single_pinyin_extarct_tone(pinyin):
    tone = 0
    raw = pinyin
    pinyin = raw.strip().lower()
    normalized = raw
    for _tone, letters in _dict['tones']['pinyin'].items():
        # Ignore the zero-tone list
        if _tone == 0:
            continue
        for char_index, char in enumerate(letters):
            if char in pinyin:
                tone_char_index = pinyin.index(char)
                tone = _tone
                normalized = pinyin[:tone_char_index] \
                           + _dict['tones']['pinyin'][0][char_index] \
                           + pinyin[tone_char_index+1:]
                break
        else:
            continue
        break
    return normalized, tone
