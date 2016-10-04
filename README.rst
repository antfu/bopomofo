Bopomofo
==========

Translate 漢字 to ㄅㄆㄇㄈ

based on `lxneng/xpinyin <https://github.com/lxneng/xpinyin>`_.

Install
----------

::

    pip install xpinyin


Usage
----------

::

    >>> from bopomofo import to_bopomofo
    >>> to_bopomofo(u'注音')
    'ㄓㄨ、ㄧㄣ'

    >>> p.get_pinyin(u'注音', tone_marks=False)
    'ㄓㄨ、ㄧㄣ'

    >>> to_bopomofo(u'注音', ' ')
    'ㄓㄨ ㄧㄣ'
