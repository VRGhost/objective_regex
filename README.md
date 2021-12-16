Python objective regular expression library
==============================

[![CI](https://github.com/VRGhost/objective_regex/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/VRGhost/objective_regex/actions/workflows/main.yml)

* Do you work with regular expressions often?
* Do you want for them to me better readable and easier to support?

So do I. Tired of writing of ugly mixture of backslashes, brackets and odd symbols, I have started to wonder if there is a better, more elegant way of dealing with them.

And here is result of my thought!

This library is implementation of object-oriented approach of constructing regular expressions.



Usage examples
--------

Let's start with construction of a few simple examples.

    >>> import ObjectiveRegex as ORe
    >>> _objectiveReg = ORe.Text("Hello world!")
    >>> print repr(_objectiveReg)
    <Text 'Hello world!'>
    
As you can see, we have constructed object named `_objectiveReg` of a `Text` class. 
`Text` class is meant for containing of a primitive text strings that are matched using _exact_ matching.

So, how do we construct the actual regular expression pattern out of this objective regexp?
Easy. All objective regexp instances have `getRegex()` API function that returns regexp representation of given objective regexp.

    >>> print repr(_objectiveReg.getRegex())
    'Hello world!'

for your convinience, there is also the `getCompiled()` API function that returns the `re.compiled` object that matches that regexp pattern. It has one optional `flags` argument that is designed to accept the very same value you have been passing to the `re.compile` call. Please see [Python documentation](http://docs.python.org/library/re.html#contents-of-module-re) for the list of its possible values.


As you can see, the `Text` class automatically escapes all symbols that have special meaning:

    >>> print ORe.Text("^.*$").getRegex()
    \^\.\*\$
    
So you can safely assume that any string within `Text` class will be matched exaly.

But what if one wants to construct objective regex using textual regular expression as one of its elements?
Well, there is `Raw` class to do that. It always resolves to exactly same string than the one it was constructed from.

    >>> print ORe.Raw("^.*$").getRegex()
    ^.*$
    
As you can see, the difference in behaviour is exactly as one might have expected:

    >>> print ORe.Raw("^.*$").getCompiled().match("Hello world!")
    <_sre.SRE_Match object at 0x01B0DF38>
    >>> print ORe.Text("^.*$").getCompiled().match("Hello world!")
    None
    >>> print ORe.Text("^.*$").getCompiled().match("^.*$")
    <_sre.SRE_Match object at 0x01B0DF38>
    >>> print ORe.Text("^.*$").getCompiled().match("^.*")
    None    
    
`Raw` regex matches any sequence of characters, while `Text` matches only one that it was provided with.

Let's see more sophisticated examples.

Constructing index-accessed groups:

    >>> print repr(ORe.Text("hello").asGroup().getRegex())
    '(hello)'
    
Name-accessed groups:

    >>> print repr(ORe.Text("hello").asGroup("group_name").getRegex())
    '(?P<group_name>hello)'
    
Joining parts of regexp together:

    >>> _reg = ORe.Text("hello") + ORe.Raw("\s+") + ORe.Text("world!")
    >>> print _reg.getRegex()
    (?:(?:hello)(?:\s+)(?:world!))
    
Matching repeating patterns:

    >>> _reg = ORe.Text("hello").times.any() + ORe.Raw("\s").times(5) + ORe.Text("world!").times.many()
    >>> print _reg.getRegex()
    (?:(?:(?:hello)*)(?:(?:\s){5})(?:(?:world!)+))
    
Referencing group in the regexp:

    >>> _hello = ORe.Text("hello").asGroup()
    >>> _reg = _hello + ORe.Text("world").asGroup("wrld") + _hello
    >>> print _reg.getRegex()
    (?:(?:(hello))(?:(?P<wrld>world))\1)

Referencing named group is done in the same way:

    >>> _hello = ORe.Text("hello").asGroup("hello_group")
    >>> _reg = _hello + ORe.Text("world").asGroup("wrld") + _hello
    >>> print _reg.getRegex()
    (?:(?:(?P<hello_group>hello))(?:(?P<wrld>world))(?P=hello_group))
    
Construction of a regexp that matches ether `hello_world_bye` of `world_no_hello`:

    >>> _hello = ORe.Text("hello").asGroup()
    >>> _reg = _hello + ORe.Text("_world_") + ORe.If(_hello, "bye", "no_hello")
    >>> print _reg.getRegex()
    (?:(?:(hello))(?:_world_)(?(1)(?:bye)|(?:no_hello)))
    
Expression that matches any one of provided regular expressions:

    >>> _reg = ORe.ops.Any(["op1", "op2", "op3"])
    >>> print _reg.getRegex()
    (?:op1)|(?:op2)|(?:op3)

The text string can be used as an operand for any regular expression. In such case, this text string is casted to the `Text` class, thus resulting regexp will all special symbols, that were collected from plain `string` instances, properly escaped.

    >>> _reg = "hello! .* world " + ORe.Raw(".*") + " [a-z] something"
    >>> print _reg.getRegex()
    (?:(?:(?:hello! \.\* world )(?:.*))(?: \[a-z\] something))

