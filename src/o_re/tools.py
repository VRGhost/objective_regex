from . import symbols


def space_sep(words, strict=True):
    _out = None

    if strict:
        _sep = symbols.Space.times.many()
    else:
        _sep = symbols.Space.times.any()

    for _word in words:
        if _out is None:
            _out = _word
        else:
            _out += _sep + _word

    return _out


def force_full_line(reg, strict=True):
    if strict:
        return symbols.Sol + reg + symbols.Eol
    else:
        return space_sep((symbols.Sol, reg, symbols.Eol), False)
