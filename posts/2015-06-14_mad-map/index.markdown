---
tags: [python, map, design]
summary: >-
  A short essay about map() function design in Python, why it's horrible and
  non-obvious at the first glance.
aliases: /2015/06/14/mad-map/
---

Mad Map: Python Road
====================

I use Python for several years and I used to think there was nothing in
the language that can surprise me. It was so until recently. The story
I want to tell is about how even so simple and well-known thing like `map()`
function can surprise you after years of using, and why I believe it has
a bad design.

So, what's wrong with `map()`? We use it everyday and everywhere, and it
seems OK, and none of us met any problems. Yes, indeed, `map()` works
just fine if you use it how it's intended to be used. For instance, if
you use `map()` to multiply each element of some sequence by 2 -

```python
x = map(lambda a: 2 * a, [1, 2])
```

Just keep going, everything's ok. But let me show another usage example -

```python
x = map(None, ['a', 'b', 'c'], [1, 2])
```

Can you tell now what is `x`, ha? I always thought that `map()` function
receives precisely two arguments:

 * a function to apply;
 * a sequence to be processed.

Can you imagine how I was surprised when it turned out that I was wrong?
But the most interesting part was further.

I started guessing how `map()` should behave in this case. What `None` may
mean? I recall that if we pass `None` as a function argument to `filter()`
then it will return only those elements which are equal to `True` in
boolean context. Hm, Perhaps `map()` behaves similar to `filter()`, and
will return a list of booleans? Let's check.

```python
>>> map(None, [-1, 0, 1])
[-1, 0, 1]
```

No, it's not :( So I went to the documentation and learned that if a function
argument is `None`, the identity function is assumed. In other words it's
equal to the following call -

```python
>>> map(lambda a: a, [-1, 0, 1])
[-1, 0, 1]
```

Wait a minute. `None` means identity?! Does it make sense? Perhaps if we're
talking about default behaviour, but it makes no sense from user point of
view. You know, it looks like "pass `None` if you want to get identity
function behaviour". But let's go on.

I continued guessing about how `map()` should deal with two iterables? It
was obvious to me that `map()` should chain them: when first is over,
the second will be used.

Let's back to the original code and original question.

```python
x = map(None, ['a', 'b', 'c'], [1, 2])
```

What is `x`? Taking into account that was written above I was expecting
`x` to be -

```python
['a', 'b', 'c', 1, 2]
```

Boom! I missed again, because `x` was -

```python
[('a', 1), ('b', 2), ('c', None)]
```

And I stunned because that means these two iterables were zipped, not
chained. Why zipped? I never asked for this! Is this really Python?
I always liked this language because of good design and good intentions.
And when I didn't know something it always fitted my expectations, but
this is something really weird.

I agree that someone may expect iterables to be zipped, but I'm upset
about opportunity itself to meet such unobvious construction. I wish
`map()` to be plain and simple: receive one function and one iterable,
and leave zipping or chaining up to programmers. Moreover, I wish a
function argument to be always a function, no way to fallback to default
behaviour. If someone wants identity behaviour let's pass it explicitly,
no way to do it through `None`.

The most frustrating thing is that it wasn't removed in Python 3, but
changed! First, you can't use `None` as identity function anymore
(alleluia). If you try to do that you'll fall with `TypeError` exception:

```
TypeError: 'NoneType' object is not callable
```

Second, iterables are zipped by `zip()`, not `zip_longest()`. If the
first change seems rational, the second one is mad. It doesn't provide
any benefits, but may cause a lot of pain for those who porting some
software to Python. Why? You see, if two iterables are equal in size
the behavior is still the same -

 | language / expression | `map(lambda x: x, ['a', 'b'], [1, 2])` |
 | --------------------- | -------------------------------------- |
 | Python 2              | `[('a', 1), ('b', 2)]`                 |
 | Python 3              | `[('a', 1), ('b', 2)]`                 |

if not, it's different -

 | language / expression | `map(lambda x: x, ['a', 'b', 'c'], [1, 2])` |
 | --------------------- | ------------------------------------------- |
 | Python 2              | `[('a', 1), ('b', 2), ('c', None)]`         |
 | Python 3              | `[('a', 1), ('b', 2)]`                      |

I'm really really sad about such a mad `map()` and I wish I never knew
about that. I don't know why it was designed so, but I hope none of
pythonistas will use it and one day it will be removed from the language.
