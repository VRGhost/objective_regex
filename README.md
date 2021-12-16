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

    >>> import o_re
    >>> _objectiveReg = o_re.Text("Hello world!")
    >>> print(repr(_objectiveReg))
    <Text 'Hello world!'>
    
As you can see, we have constructed object named `_objectiveReg` of a `Text` class. 
`Text` class is meant for containing of a primitive text strings that are matched using _exact_ matching.

So, how do we construct the actual regular expression pattern out of this objective regexp?
Easy. All objective regexp instances have `getRegex()` API function that returns regexp representation of given objective regexp.

    >>> print(repr(_objectiveReg.get_regex()))
    'Hello world!'

for your convinience, there is also the `getCompiled()` API function that returns the `re.compiled` object that matches that regexp pattern. It has one optional `flags` argument that is designed to accept the very same value you have been passing to the `re.compile` call. Please see [Python documentation](http://docs.python.org/library/re.html#contents-of-module-re) for the list of its possible values.


As you can see, the `Text` class automatically escapes all symbols that have special meaning:

    >>> print(o_re.Text("^.*$").get_regex())
    \^\.\*\$
    
So you can safely assume that any string within `Text` class will be matched exaly.

But what if one wants to construct objective regex using textual regular expression as one of its elements?
Well, there is `Raw` class to do that. It always resolves to exactly same string than the one it was constructed from.

    >>> print(o_re.Raw("^.*$").get_regex())
    ^.*$
    
As you can see, the difference in behaviour is exactly as one might have expected:

    >>> print(o_re.Raw("^.*$").get_compiled().match("Hello world!"))
    <re.Match object; span=(0, 12), match='Hello world!'>
    >>> print(o_re.Text("^.*$").get_compiled().match("Hello world!"))
    None
    >>> print(o_re.Text("^.*$").get_compiled().match("^.*$"))
    <re.Match object; span=(0, 4), match='^.*$'>
    >>> print(o_re.Text("^.*$").get_compiled().match("^.*"))
    None    
    
`Raw` regex matches any sequence of characters, while `Text` matches only one that it was provided with.

Let's see more sophisticated examples.

Constructing index-accessed groups:

    >>> print(repr(o_re.Text("hello").as_group().get_regex()))
    '(hello)'
    
Name-accessed groups:

    >>> print(repr(o_re.Text("hello").as_group("group_name").get_regex()))
    '(?P<group_name>hello)'
    
Joining parts of regexp together:

    >>> _reg = o_re.Text("hello") + o_re.Raw("\s+") + o_re.Text("world!")
    >>> print(_reg.get_regex())
    (?:(?:(?:hello)(?:\s+))(?:world!))
    
Matching repeating patterns:

    >>> _reg = o_re.Text("hello").times.any() + o_re.Raw("\s").times(5) + o_re.Text("world!").times.many()
    >>> print(_reg.get_regex())
    (?:(?:(?:(?:hello)*)(?:(?:\s){5}))(?:(?:world!)+)
    
Referencing group in the regexp:

    >>> _hello = o_re.Text("hello").as_group()
    >>> _reg = _hello + o_re.Text("world").as_group("wrld") + _hello
    >>> print(_reg.get_regex())
    (?:(?:(?:(hello))(?:(?P<wrld>world)))(?:\1))

Referencing named group is done in the same way:

    >>> _hello = o_re.Text("hello").as_group("hello_group")
    >>> _reg = _hello + o_re.Text("world").as_group("wrld") + _hello
    >>> print(_reg.get_regex())
    (?:(?:(?:(?P<hello_group>hello))(?:(?P<wrld>world)))(?:(?P=hello_group)))
    
Construction of a regexp that matches ether `hello_world_bye` of `world_no_hello`:

    >>> _hello = o_re.Text("hello").as_group()
    >>> _reg = _hello + o_re.Text("_world_") + o_re.If(_hello, "bye", "no_hello")
    >>> print(_reg.get_regex())
    (?:(?:(?:(hello))(?:_world_))(?:(?(1)(?:bye)|(?:no_hello)))
    
Expression that matches any one of provided regular expressions:

    >>> _reg = o_re.ops.Any(["op1", "op2", "op3"])
    >>> print(_reg.get_regex())
    (?:op1)|(?:op2)|(?:op3)

The text string can be used as an operand for any regular expression. In such case, this text string is casted to the `Text` class, thus resulting regexp will all special symbols, that were collected from plain `string` instances, properly escaped.

    >>> _reg = "hello! .* world " + o_re.Raw(".*") + " [a-z] something"
    >>> print(_reg.get_regex())
    (?:(?:(?:hello! \.\* world )(?:.*))(?: \[a-z\] something)

