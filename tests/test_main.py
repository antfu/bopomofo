# -*- coding: utf-8 -*-
import pytest
import bopomofo


def test_application():
    assert bopomofo.to_bopomofo(u'注音') == u'ㄓㄨˋ ㄧㄣ'
    assert bopomofo.to_bopomofo(u'注音', u'、') == u'ㄓㄨˋ、ㄧㄣ'
    assert bopomofo.to_bopomofo(u'注音', tones=False) == u'ㄓㄨ ㄧㄣ'
    assert bopomofo.to_bopomofo(u'注音', first_tone_symbol=True) == u'ㄓㄨˋ ㄧㄣˉ'
    assert bopomofo.to_bopomofo(u'English') == 'English'
    assert bopomofo.to_bopomofo(u'English中文') == u'English ㄓㄨㄥ ㄨㄣˊ'
    assert bopomofo.to_bopomofo(u'GitHub是一個透過Git進行版本控制的軟體原始碼代管服務', u'', first_tone_symbol=True) \
        == u'GitHubㄕˋㄧˉㄍㄜˋㄊㄡˋㄍㄨㄛˋGitㄐㄧㄣˋㄒㄧㄥˊㄅㄢˇㄅㄣˇㄎㄨㄥˋㄓˋㄉㄜ˙ㄖㄨㄢˇㄊㄧˇㄩㄢˊㄕˇㄇㄚˇㄉㄞˋㄍㄨㄢˇㄈㄨˊㄨˋ'


def test_extract_tone():
    cases = [
        [u'fú', 'fu', 2],
        [u'wù', 'wu', 4],
        [u'shì', 'shi', 4],
        [u'yī', 'yi', 1],
        [u'tòu', 'tou', 4],
        [u'a', 'a', 0]
    ]

    for case in cases:
        normalized, tone = bopomofo._single_pinyin_extarct_tone(case[0])
        assert normalized == case[1]
        assert tone == case[2]


def test_pinyin_to_bopomofo():
    cases = [
        [u'fú', u'ㄈㄨˊ'],
        [u'wù', u'ㄨˋ'],
        [u'shì', u'ㄕˋ'],
        [u'yī', u'ㄧ'],
        [u'tòu', u'ㄊㄡˋ']
    ]

    for case in cases:
        assert bopomofo._single_pinyin_to_bopomofo(
            case[0], tones=True) == case[1]


def test_bopomofo_to_pinyin():
    cases = [
        [u'fú', u'ㄈㄨˊ'],
        [u'wù', u'ㄨˋ'],
        [u'shì', u'ㄕˋ'],
        [u'yī', u'ㄧ'],
        [u'tòu', u'ㄊㄡˋ']
    ]

    for case in cases:
        assert bopomofo._single_bopomofo_to_pinyin(
            case[1], tones=True) == case[0]

    with pytest.raises(bopomofo.PinyinParsingError):
        bopomofo._single_bopomofo_to_pinyin('ㄕㄕ')

    with pytest.raises(bopomofo.PinyinParsingError):
        bopomofo._single_bopomofo_to_pinyin('ㄜㄜ')

    assert bopomofo.bopomofo_to_pinyin(u'GitHubㄕˋㄧˉㄍㄜˋㄊㄡˋㄍㄨㄛˋGitㄐㄧㄣˋㄒㄧㄥˊㄅㄢˇㄅㄣˇㄎㄨㄥˋㄓˋㄉㄜ˙ㄖㄨㄢˇㄊㄧˇㄩㄢˊㄕˇㄇㄚˇㄉㄞˋㄍㄨㄢˇㄈㄨˊㄨˋ') \
        == u'GitHub shì yī gè tòu guò Git jìn xíng bǎn běn kòng zhì de ruǎn tǐ yuán shǐ mǎ dài guǎn fú wù'
    assert bopomofo.bopomofo_to_pinyin(u'GitHubㄕˋㄧˉㄍㄜˋㄊㄡˋㄍㄨㄛˋGitㄐㄧㄣˋㄒㄧㄥˊㄅㄢˇㄅㄣˇㄎㄨㄥˋㄓˋㄉㄜ˙ㄖㄨㄢˇㄊㄧˇㄩㄢˊㄕˇㄇㄚˇㄉㄞˋㄍㄨㄢˇㄈㄨˊㄨˋ', tones=False) \
        == u'GitHub shi yi ge tou guo Git jin xing ban ben kong zhi de ruan ti yuan shi ma dai guan fu wu'


def test_to_pinyin():
    assert bopomofo.to_pinyin(u'GitHub是一個透過Git進行版本控制的軟體原始碼代管服務', tones=True) \
        == u'GitHub shì yī gè tòu! guò! Git jìn xíng bǎn běn kòng zhì de ruǎn tǐ yuán shǐ mǎ dài guǎn fú wù'
    assert bopomofo.to_pinyin(u'GitHub是一個透過Git進行版本控制的軟體原始碼代管服務') \
        == u'GitHub shi yi ge tou guo Git jin xing ban ben kong zhi de ruan ti yuan shi ma dai guan fu wu'


def test_invaild_inputs():
    with pytest.raises(bopomofo.PinyinParsingError):
        bopomofo._single_pinyin_to_bopomofo('hee')

    with pytest.raises(bopomofo.PinyinParsingError):
        bopomofo._single_pinyin_to_bopomofo('vvv')
