<!-- Bytes, strings, wrath and encodings! -->

### Байты, строки, гнев и Python

Игорь Кальницкий ~
[@ikalnytskyi](https://github.com/ikalnytskyi)

---

Неписанные истины о Python

- Python такой **крутой**, что многие преобразования (явные и неявные)
  из байт в строки и наоборот берет на себя.

  <!-- .element: class="fragment" -->

- Python такой **плохой**, что многие преобразования (явные и неявные)
  из байт в строки и наоборот берет на себя.

  <!-- .element: class="fragment" -->

---

Paramiko 2.1.1 (forks 872, stars 3126)

```python
try:
    t, data = self._read_packet()
except EOFError:
    self._log(DEBUG, 'EOF -- end of session')
    return
except Exception as e:
    self._log(DEBUG, 'Exception on channel: ' + str(e))
    self._log(DEBUG, util.tb_strings())
    return
```

---

Pelican 3.7.1 (forks 1341, stars 6505)

```python
parser.add_argument('-p', '--path', default=_DEFAULT_PATH,
                    help="The path to generate the blog into")
parser.add_argument('-t', '--title', metavar="title",
                    help='Set the title of the website')
parser.add_argument('-a', '--author', metavar="author",
                    help='Set the author name of the website')
```

---

<!-- .slide: data-background="#974031" class="statement" -->

Крупные и зрелые проекты тоже работают со строками и кодировками
неправильно.

>>>

![Neo, The One](images/neo.png)

«There is no ~~spoon~~ string.»

---

<!-- .slide: data-background="#974031" class="statement" -->

Строка – это абстракция вокруг массива байт, призванная упростить операции
с текстом.

---

![single-byte encoding](images/single-byte-enc.svg)

- ASCII (7 бит)
- Windows 1251 (8 бит)
- KOI8-U (8 бит)

<!-- .element: class="fragment" -->

---

| Windows 1251  | Latin-1 | KOI8-R |
| ------------- | ------- | ------ |
| привет        | ïðèâåò  | ОПХБЕР |

---

<!-- .slide: data-background="#974031" class="statement" -->

Однобайтовые кодировки способны отобразить только один язык (или группу
языков), не считая ASCII*.

---

![Unicode](images/unicode.svg)

«One ~~ring~~ standard to rule them all.»

---

![unicode wonder](images/unicode-meme.png)

---

- Universal Coded Character Set, >=128000 символов.
- Способы кодирования символов из UCS.
- Примеры, правила нормализации и прочее.

---

![fixed-length encoding](images/fixed-len-enc.svg)

- UCS-2 (16 бит)
- UCS-4, UTF-32 (32 бит)

<!-- .element: class="fragment" -->

---

<!-- .slide: data-background="#974031" class="statement" -->

Многобайтовые кодировки с фиксированным размером занимают много места
на диске и в памяти.

---

![variable-length encoding](images/var-len-enc.svg)

- UTF-8 (8-32 бит)
- UTF-16 (16, 32 бит)

---

<!-- .slide: data-background="#974031" class="statement" -->

UTF-8 тут, UTF-8 там.

>>>

### Строки и Python

---

```python
>>> text = "я batмен"

>>> type(text)
<type 'str'>

>>> print(text)
я batмен
```

---

```text
$ python app.py
� ������
```

```text
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'latin-1' codec can't encode character u'\u044f' in position 0: ordinal not in range(256)
```

```text
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x82 in position 0: invalid start byte
```

---

| Тип       | Литерал  | Описание        |
| --------- | -------- | --------------- |
| `str`     | `"abc"`  | cтрока          |
| `unicode` | `u"αβγ"` | unicode строка  |
| `bytes`   | `b"abc"` | `str` псевдоним |

Python 2

---

| Тип       | Литерал              | Описание        |
| --------- | -------------------- | --------------- |
| `str`     | `"αβγ"` или `u"αβγ"` | unicode строка  |
| `bytes`   | `b"abc"`             | байты           |

Python 3

---

Python 2

```
>>> 'Я'
'\xd0\xaf'

>>> u'Я'
u'\u042f'
```

Python 3

```
>>> 'Я'
u'\u042f'

>>> u'Я'
u'\u042f'
```

---

<!-- .slide: data-background="#974031" class="statement" -->

В Python 2 тип "str" представляет собой байты, хоть и имеет строковый
интерфейс.

---

Байты ↔ Строки

- `.encode(...)` преобразовывает строку в байты

  ```python
  >>> 'αβγ'.encode('utf-8')
  b'\xce\xb1\xce\xb2\xce\xb3'
  ```

- `.decode(...)` преобразовывает байты в строку

  ```python
  >>> b'\xce\xb1\xce\xb2\xce\xb3'.decode('utf-8')
  'αβγ'
  ```

---

```python
>>> b'\xce\xb1\xce\xb2\xce\xb3'.decode('utf-8')
'αβγ'

>>> b'\xce\xb1\xce\xb2\xce\xb3'.decode('utf-16')
'뇎닎돎'
```

WTF?

---

<!-- .slide: data-background="#974031" class="statement" -->

Байты невозможно восстановить в строку без знания исходной кодировки.

>>>

### Типичные ошибки

---

```python
>>> text = 'привет'
>>> unicode(text)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'ascii' codec can't decode byte 0xd0 in position 0: ordinal not in range(128)
```

```python
>>> unicode(text, encoding)
u'\u043f\u0440\u0438\u0432\u0435\u0442'
>>> text.decode(encoding)
u'\u043f\u0440\u0438\u0432\u0435\u0442'
```
<!-- .element: class="fragment" -->

---

<!-- .slide: data-background="#974031" class="statement" -->

Никогда не полагайтесь на кодировку по-умолчанию при конвертации из байт
в строку.

---

Paramiko 2.1.1 (forks 872, stars 3126)

```python
try:
    t, data = self._read_packet()
except EOFError:
    self._log(DEBUG, 'EOF -- end of session')
    return
except Exception as e:
    self._log(DEBUG, 'Exception on channel: ' + str(e))
    self._log(DEBUG, util.tb_strings())
    return
```

---

Python 2

```python
>>> e = Exception(u'/home/user/документ.json')
>>> str(e)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 11-18: ordinal not in range(128)
```

---

Python 2

```python
>>> e = Exception(u'/home/user/документ.json')

>>> unicode(e)
u'/home/user/\u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442.json'

>>> import six
>>> six.text_type(e)
u'/home/user/\u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442.json'
```

---

<!-- .slide: data-background="#974031" class="statement" -->

Всегда работайте с unicode строками внутри вашего приложения.

---

Pelican 3.7.1 (forks 1341, stars 6505)

```python
parser.add_argument('-p', '--path', default=_DEFAULT_PATH,
                    help="The path to generate the blog into")
parser.add_argument('-t', '--title', metavar="title",
                    help='Set the title of the website')
parser.add_argument('-a', '--author', metavar="author",
                    help='Set the author name of the website')
```

---

![Unix Terminal Flow](images/unix-terminal-flow.svg)

- Терминал преобразовывает введенный текст в байты согласно выставленной
  в настройках кодировке.

- Терминал преобразовывает полученные байты в текст согласно выставленной
  в настройках кодировке.

---

<!-- .slide: data-background="#974031" class="statement" -->

UNIX приложение коммуницирует с внешним миром посредством байт.

---

Python 2

```python
>>> type(sys.argv[0])
<type 'str'>
```

Python 3

```python
>>> type(sys.argv[0])
<type 'str'>
```

---

Как узнать кодировку терминала?

---

<!-- .slide: data-background="#974031" class="statement" -->

Кодировку терминала определить невозможно. Наиболее приближенное – кодировка
локали.

---

Фикс?

```python
import locale

def _to_unicode(v):
    if six.PY2:
        return v.decode(locale.getpreferredencoding())
    return v

parser.add_argument('-t', '--title', metavar="title",
                    type=_to_unicode,
                    help='Set the title of the website')
```

---

<!-- .slide: data-background="#974031" class="statement" -->

Python 3 конвертирует CLI аргументы из байт в строки используя
'sys.getfilesystemencoding()'.

---

- `sys.getfilesystemencoding()`

  - Linux: кодировка локали
  - macOS: `utf-8`
  - Windows: `utf-8`, `mbcs`

---

Фикс!

```python
import locale

def _to_unicode(v):
    if six.PY2:
        return v.decode(locale.getpreferredencoding())

    fsenc = sys.getfilesystemencoding()
    lcenc = locale.getpreferredencoding()
    return v.encode(fsenc, 'surrogateescape').decode(lcenc)

parser.add_argument('-t', '--title', metavar="title",
                    type=_to_unicode,
                    help='Set the title of the website')
```

---

Обработчики ошибок Unicode

- `strict`
- `ignore`
- `replace`
- `surrogateescape`

---

<!-- .slide: data-background="#974031" class="statement" -->

'surrogateescape' строки невозможно отобразить на экране и отличить от
unicode строк.

>>>

### Как избежать проблем?

---

<!-- .slide: data-background="#974031" class="statement" -->

![unicode hamburger](images/unicode-hamburger.svg)

---

<!-- .slide: data-background="#974031" class="statement" -->

В Python 2 используйте unicode литерал для создания строк.

---

<!-- .slide: data-background="#974031" class="statement" -->

Тестируйте вход и выход вашего приложения с использованием ASCII несовместимых
символов.

---

<!-- .slide: data-background="#974031" class="statement" -->

Тестируйте вход и выход вашего приложения при разных кодировках локали.

---

<!-- .slide: data-background="#974031" class="statement" -->

Осознайте всю эту чепуху, что я рассказал. :)

>>>

Спасибо за внимание! Вопросы?

<ihor@kalnytskyi.com>
