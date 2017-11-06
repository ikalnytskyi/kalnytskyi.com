![](images/di.png)

# Dependency Injection Pythonic Way

<small>or how I wrote [Picobox](https://picobox.readthedocs.io/)</small>

---

<!-- .slide: data-background="#2a76dd" -->

## What's dependency injection?

---

![DI definition by Martin Fowler](images/di-fowler.gif)

> The basic idea of the Dependency Injection is to have a separate object, an
> assembler, that populates a field in the lister class with an appropriate
> implementation for the finder interface [...]
>
> -- [Martin Fowler](https://martinfowler.com/articles/injection.html)

---

![DI definition by Wikipedia](images/di-wiki.jpg)

> In software engineering, dependency injection is a technique whereby one
> object supplies the dependencies of another object. A dependency is an object
> that can be used (a service) [...]
>
> -- [Wikipedia](https://en.wikipedia.org/wiki/Dependency_injection)

---

\- DI -

```python
def spam(sender):
    sender.send('spam!')

sender = Sender()
spam(sender)
```

\- Not DI -

```python
def spam():
    sender = Sender()
    sender.send('spam!')

spam()
```

---

> "Dependency Injection" is a 25-dollar term for a 5-cent concept.
>
> -- [James Shore](http://www.jamesshore.com/Blog/Dependency-Injection-Demystified.html)

>>>

<!-- .slide: data-background="#2a76dd" -->

## Why do we need DI frameworks?

---

* To wire up complex object relationships.

* To control when an object is created.
  <!-- .element: class="fragment" -->

* To control how many instances are created.
  <!-- .element: class="fragment" -->

>>>

<!-- .slide: data-background="#2a76dd" -->

## What do we have in Python?

---

* dependency-injector
* pinject
* injector
* inject
* ...

---

* dependency-<em>inject</em>or
* p<em>inject</em>
* <em>inject</em>or
* <em>inject</em>
* ...

---

##### dependency-injector

```python
import dependency_injector.providers as providers
import dependency_injector.containers as containers

class Sender:
    def send(self, text):
        print(text)

def spam(sender):
    sender.send('spam')

class Senders(containers.DeclarativeContainer):
    sender = providers.ThreadLocalSingleton(Sender)

class Application(containers.DeclarativeContainer):
    spam = providers.Callable(spam, sender=Senders.sender)

Application.spam()
```

---

* 😕 Everything needs to be wrapped into containers.

* 😕 No easy way to change configuration.

* 😕 Providers' override() has Mock decease.

---

#### pinject

```python
import pinject

class Sender(object):
    def send(self, text):
        print(text)

class Spammer(object):
    def __init__(self, sender):
        self._sender = sender
    def spam(self):
        self._sender.send('spam')

class Configure(pinject.BindingSpec):
    def configure(self, bind):
        bind('sender', to_class=Sender, in_scope=pinject.SINGLETON)

graph = pinject.new_object_graph(binding_specs=[Configure()])
spammer = graph.provide(Spammer)
spammer.spam()
```

---

* 😕 Abandoned; does not work on Python 3.

* 😕 Only \__init__ arguments can be injected.

* 🙂 Custom BindingSpec can override values in tests.

* 😕 Confusing implicit (default) binding rules.

---

#### injector

```python
import injector

class Sender:
    def send(self, text):
        print(text)

class Spammer(object):
    @injector.inject
    def __init__(self, sender: Sender):
        self._sender = sender

    def spam(self):
        self._sender.send('spam')

def configure(binder):
    binder.bind(Sender, scope=injector.threadlocal)

the_injector = injector.Injector(configure)
spammer = the_injector.get(Spammer)
spammer.spam()
```

---

* 😕 Type annotations are used as injection keys.

* 😕 Only \__init__ arguments can be injected.

* 🙂 call_with_injection() can set custom injector in tests.

---

##### inject

```python
import inject

class Sender:
    def send(self, text):
        print(text)

@inject.params(sender=Sender)
def spam(sender):
    sender.send('spam')

def configure(binder):
    binder.bind_to_constructor(Sender, Sender)

inject.configure(configure)

spam()
```

---

* 😕 No scopes.

* 🙂 Any callable is supported.

* 😕 clear_and_configure() can't be partially applied.

* 😕 One global injector instance.

>>>

<!-- .slide: data-background="#2a76dd" -->

Enter

![Picobox](images/picobox.svg)

### Picobox

---

#### Key Principles

* Simple is better than complex.

* Explicit is better than implicit.
  <!-- .element: class="fragment" -->

* Readability counts.
  <!-- .element: class="fragment" -->

* Ease of integration matters.
  <!-- .element: class="fragment" -->

---

#### So I began designing...

![Designing](images/designing-picobox.png)

---

```python
import picobox

box = picobox.Box()
box.put('foo', 42)

@box.pass_('foo')
def spam(foo):
    return foo

print(box.get('foo'))   # 42

print(spam())           # 42
print(spam(13))         # 13
print(spam(foo=99))     # 99
```

---

```python
import picobox

box = picobox.Box()
box.put('foo', 42)

@box.pass_('foo')
def spam(foo):
    return foo

@box.pass_('foo', as_='bar')
def eggs(bar):
    return bar

print(box.get('foo'))   # 42

print(spam())           # 42
print(eggs())           # 42
```

---

```python
import picobox
import random

box = picobox.Box()
box.put('foo', factory=lambda: random.choice(['spam', 'eggs']))

@box.pass_('foo')
def spam(foo):
    return foo

print(spam())           # spam
print(spam())           # eggs
print(spam())           # eggs
print(spam())           # spam
print(spam())           # eggs
```

---

```python
import picobox
import random
import threading

box = picobox.Box()
box.put('bar', factory=random.random, scope=picobox.singleton)

@box.pass_('bar')
def eggs(bar):
    print(bar)

# prints
# > 0.5333214411659912
# > 0.5333214411659912
for _ in range(2):
    threading.Thread(target=eggs).start()
```

---

```python
import picobox

@picobox.pass_('foo')
def spam(foo):
    return foo

box = picobox.Box()
box.put('foo', 13)

with picobox.push(box):
    print(spam())                                   # 13

    with picobox.push(picobox.Box()) as overbox:
        overbox.put('foo', 42)
        print(spam())                               # 42

    print(spam())                                   # 13

spam()                                              # RuntimeError
```

---

![Yo Dawg!](images/di-yo-dawg.jpg)

---

```python
import picobox

@picobox.pass_('conf')
def create_session(conf):
    class Session:
        connection = conf['connection']
    return Session()

@picobox.pass_('session')
def compute(session):
    print(session.connection)

box = picobox.Box()
box.put('session', factory=create_session)
box.put('conf', {'connection': 'sqlite://'})

with picobox.push(box):
    compute()
```

>>>

<!-- .slide: data-background="#2a76dd" -->

## Why Picobox?

---

* Scopes (e.g. singleton, threadlocal).

* Replaceable containers (i.e. boxes).
  <!-- .element: class="fragment" -->

* Thread-safe.
  <!-- .element: class="fragment" -->

* Lightweight (~140 LOC).
  <!-- .element: class="fragment" -->

* Zero dependencies.
  <!-- .element: class="fragment" -->

* Pure Python.
  <!-- .element: class="fragment" -->

>>>

## QA?

<small>
  ask <ihor@kalnytskyi.com>
</small>
