# form .
from .text import Raw

##Magical custom symbols

Any = Raw('.')
Sol = Raw('^') # Start Of Line
Eol = Raw('$')
Space = Raw("\s")
Spaces = Space.times.many()

# vim: set sts=4 sw=4
