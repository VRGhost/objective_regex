from .text import Raw

# Magical custom symbols

Any = Raw('.')
Sol = Raw('^')  # Start Of Line
Eol = Raw('$')
Space = Raw(r"\s")
Spaces = Space.times.many()
