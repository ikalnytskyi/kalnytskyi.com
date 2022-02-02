---
summary: |
  A simple trick on how to check that strings matches certain pattern using
  pytest.
aliases: /howto/assert-str-matches-regex-in-pytest/
---

Assert that str matches regex in pytest
=======================================

Once in a while every Pythonista faces a need to test that some string value
matches a regex pattern. When it comes we have no option but to use `re` module
directly.

```python
import re

def test_something_very_useful():
    value = get_some_string()
    assert re.match('\d+', value)
```

While it works fine in case of lone string, it's not always convenient to do
the same when a string is a part of more complex data structure (e.g. `dict`),
because you need to extract the string, check it and only then get back to
check rest attributes.

```python
import re

def test_something_even_more_useful():
    mapping = get_some_structure()

    # inconvenient and boring! :(
    assert 'value' in mapping
    value = mapping.pop('value')
    assert re.match('\d+', value)

    # rest assertion
    assert mapping = {'foo': 1,
                      'bar': 2}
```

Fortunately, it's pretty easy to write convenient `pytest` helper that would
check a pattern as a part of checking the whole data structure.

```python
def test_something_even_more_useful():
    mapping = get_some_structure()
    assert mapping = {'foo': 1,
                      'bar': 2,
                      'value': pytest_regex('\d+')}
```

Looks better, huh? :) So the trick is done by the following few lines which
we're successfully using in [XSnippet API].

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

[XSnippet API]: https://github.com/xsnippet/xsnippet-api
