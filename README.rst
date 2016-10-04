Bopomofo
==========
.. image:: https://img.shields.io/travis/antfu/bopomofo.svg?style=flat-square
    :target: https://travis-ci.org/antfu/bopomofo

.. image:: https://img.shields.io/codecov/c/github/antfu/bopomofo.svg?style=flat-square
    :target: https://codecov.io/gh/antfu/bopomofo

.. image:: https://img.shields.io/pypi/v/bopomofo.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bopomofo

.. image:: https://img.shields.io/pypi/dm/bopomofo.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bopomofo

.. image:: https://img.shields.io/pypi/status/bopomofo.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bopomofo

.. image:: https://img.shields.io/pypi/l/bopomofo.svg?style=flat-square
    :target: https://github.com/antfu/bopomofo/blob/master/LICENSE


Translate 漢字 to ㄅㄆㄇㄈ, based on `lxneng/xpinyin <https://github.com/lxneng/xpinyin>`_.

Install
----------

::

    pip install bopomofo


Usage
----------

::

    >>> from bopomofo import to_bopomofo
    >>> to_bopomofo(u'注音')
    'ㄓㄨˋ、ㄧㄣ'

    >>> to_bopomofo(u'注音', tones=False)
    'ㄓㄨ、ㄧㄣ'

    >>> to_bopomofo(u'注音', ' ')
    'ㄓㄨˋ ㄧㄣ'

    >>> to_bopomofo(u'注音', ' ')
    'ㄓㄨˋ ㄧㄣ'
