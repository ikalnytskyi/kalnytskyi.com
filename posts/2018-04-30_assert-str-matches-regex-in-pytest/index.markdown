---
summary: >-
  pytest is a mature full-featured Python testing tool and test runner. In this
  post you can learn a trick how to match a string against a regular expression
  when a string is part of dict or list.
aliases: /howto/assert-str-matches-regex-in-pytest/
---

Assert that str matches regex in pytest
=======================================

Once in a while every Pythonista faces a need to test that some string value
matches a regex pattern. When it comes to it we have no option but to use `re`
module directly.

```python
import re

def test_something_very_useful():
    value = get_some_string()
    assert re.match("\d+", value)
```

While it works perfectly fine in case of a lone string, it's not always
convenient to do the same when a string is a part of more complex data
structure (e.g. `dict`) because you need to extract the string, check it and
only then get back to check rest attributes.

```python
import re

def test_something_even_more_useful():
    mapping = get_some_structure()

    # inconvenient and boring! :(
    assert "value" in mapping
    value = mapping.pop("value")
    assert re.match("\d+", value)

    # rest assertion
    assert mapping = {
        "foo": 1,
        "bar": 2,
    }
```

Fortunately, it's pretty easy to write a convenient helper that would check a
string against some pattern when comparing complex data structures.

```python
def test_something_even_more_useful():
    mapping = get_some_structure()
    assert mapping = {
        "foo": 1,
        "bar": 2,
        "value": pytest_regex("\d+"),
    }
```

Looks better, huh? :) The trick can be achieved by implementing a class wrapper
that implements both `__eq__` and `__repr__` dunder methods. The first method
is used to implement matching while the other – to return the value that will
be shown in error message in case of errors.

```python
import re

class pytest_regex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return self._regex.pattern
```

Well, actually, it's not by any means tied to `pytest` and could be used even
in non-test production code, though I found this rather queer.
