### Нельзя просто так взять и сделать версионирование API

![EatDog](images/eatdog.png)

github.com/ikalnytskyi

---

### Мотивация

- *Забота о пользователях*

>>>

![Twitter API](images/twitter-api.svg)

---

### Мотивация

- Забота о пользователях
- *Обнаружение поддерживаемого функционала*

>>>

```json
{
    "owner": "John Doe",
    "product": { ... }
}
```

```json
{
    "owner": {
        "firstName": "John",
        "lastName": "Doe"
    },
    "product": { ... }
}
```

```json
{
    "owner": {
        "firstName": "John",
        "lastName": "Doe",
        "phone": "+1 234 567 89"
    },
    "product": { ... }
}
```

>>>

```python
import requests

response = requests.get('https://api.not-ebay.com/sales')
entity = response.json()

if isinstance(entity['owner'], dict):
    if 'phone' in entity['owner']:
        # Последняя версия API, предоставляем весь
        # полный набор функционала.
    else:
        # Предпоследняя версия API, предоставляем
        # ограниченный набор функционала.
else:
    # Боль. :'( Самая старая версия API, предоставляем
    # только базовый набор функционала.
```

---

### Мотивация

- Забота о пользователях
- Обнаружение поддерживаемого функционала
- *Обновление с минимальным временем простоя*

>>>

![Rolling Upgrades](images/rolling-upgrades.svg)

---

![Studying](images/studying.png)

---

### Способы версионирования HTTP API

- *Версионирование при помощи URI*

>>>

```http
GET /v1.42/resource HTTP/1.1
Host: api.example.com
```

---

### Способы версионирования HTTP API

- Версионирование при помощи URI
- *Версионирование при помощи параметра запроса*

>>>

```http
GET /resource?version=1.42 HTTP/1.1
Host: api.example.com
```

---

### Способы версионирования HTTP API

- Версионирование при помощи URI
- Версионирование при помощи параметра запроса
- *Версионирование при помощи HTTP заголовка*

>>>

```http
GET /resource HTTP/1.1
Host: api.example.com
Api-Version: 1.42
Vary: Api-Version
```

---

### Способы версионирования HTTP API

- Версионирование при помощи URI
- Версионирование при помощи параметра запроса
- Версионирование при помощи HTTP заголовка
- *Версионирование при помощи Content Negotiation*

>>>

```http
GET /resource HTTP/1.1
Host: api.example.com
Accept: application/vnd.project+json; version=1.42
```

---

![Rockstar](images/rockstar.png)

---

### Версионирование при помощи Content Negotiation

*Заголовок `Accept` и [RFC 7231](https://tools.ietf.org/html/rfc7231)* <!-- .element: class="fragment" -->

>>>

```http
GET /resource HTTP/1.1
Host: api.example.com
Accept: application/xml; q=0.2, application/json, application/*
Accept: application/vnd.project+json; version=1; q=0.7
Accept: application/vnd.project+json; q=0.9; version=2
```

---

##### Версионирование при помощи Content Negotiation

*Content-Type дилемма* <!-- .element: class="fragment" -->

>>>

```http
POST /resource HTTP/1.1
Host: api.example.com
Accept: application/vnd.project+json; version=1
Content-Type: ???

{
    "owner": "John Doe",
    "product": { ... }
}
```

>>>


```http
POST /resource HTTP/1.1
Host: api.example.com
Accept: application/vnd.project+json; version=1
Content-Type: application/vnd.project+json; version=1

{
    "owner": "John Doe",
    "product": { ... }
}
```

>>>

```http
POST /resource HTTP/1.1
Host: api.example.com
Accept: application/vnd.project+json; version=1
Content-Type: application/vnd.project+json; version=2

{
    "owner": {
        "firstName": "John",
        "lastName": "Doe"
    },
    "product": { ... }
}
```

>>>

```http
POST /resource HTTP/1.1
Host: api.example.com
Accept: application/vnd.project+json; version=1
Content-Type: application/json

{
    "owner": "John Doe",
    "product": { ... }
}
```

>>>

Согласно [RFC 7231](https://tools.ietf.org/html/rfc7231):

- Заголовок `Accept` определяет предпочтения по типу представления ответа
  от сервера, включая запрашиваемый ресурс и возможные ошибки.

- Заголовок `Content-Type` определяет тип представления, передаваемого
  в теле сообщения данных.

---

##### Ох.. Может попробовать HTTP заголовок?

---

### Версионирование при помощи HTTP заголовка

- Какой выбрать код ответа, если запрашиваемая версия API не найдена?

  - 400 Bad Request
  - 404 Not Found
  - 406 Not Acceptable
  - 412 Precondition Failed

- Убедиться, что выбранный заголовок не фильтруется используемым стеком
  технологий.

---

##### Хм.. А что с параметром запроса?

---

### Версионирование при помощи параметра запроса

- Традиционно используются совместно с методом `GET`.

- Некоторые веб-фреймворки могут быть не готовы к такому порядку вещей.

>>>

django 1.10

```python
@require_http_methods(['POST'])
def create_user(request):
    version = request.GET.get('version', LATEST_VERSION)
```

---

##### Ок, попробуем URI

---

### Версионирование при помощи URI

- Не требует никаких специальных возможностей фреймворка. В простом случае,
  каждая версия - отдельный обработчик.

- Самый популярный способ версионирования HTTP API.

---

### Версионирование и веб-фреймворки

- Фреймворки не решают проблему версионирования API. <!-- .element: class="fragment" -->

- В лучшем случае существуют расширения к фреймворкам, которые позволяют
  автоматически извлечь версию и передать ее в обработчик.  <!-- .element: class="fragment" -->

>>>

djangorestframework 3.5.3

```python
from rest_framework import views, versioning

class CreateUser(views.APIView):

    versioning_class = versioning.QueryParameterVersioning

    def post(self, request, format=None):
        if request.version == '42':
            pass

```

---

### DIY: версионирование и веб-фреймворки

- Подход к версионированию тесно связан с подходом к организации кода.

  - Один обработчик, принимающий версию API?
  - Много обработчиков, вызываемых в зависимости от версии?

- В сочетании со способами передачи версии клиентом имеем немалое
  количество вариантов.

>>>

Решение задачи обычно сводится к написанию собственного `middleware` или
роутера.

---

![Epic Win](images/epic-win.png)

---

### Эволюция данных

- Эволюция API - это следствие эволюции данных.

- Расширение функциональности зачастую ведет к эволюции данных.

>>>

```python
database = [
    {'owner': 'John Doe',
     'product': some_product_data},
]

@app.route('/v1/sales')
def get_sales_v1():
    return jsonify(database)
```

>>>

```python
database = [
    {'owner':
         {'firstName': 'John',
          'lastName': 'Doe'},
     'product': some_product_data},
]

@app.route('/v1/sales')
def get_sales_v1():
    conv_owner = lambda o: '{firstName} {lastName}'.format(**o)
    return jsonify([
        {'owner': conv_owner(record['owner']),
         'product': record['product']}
        for record in database
    ])

@app.route('/v2/sales')
def get_sales_v2():
    return jsonify(database)
```

---

### Эволюция тестов

Вместе с эволюцией данных следует эволюция тестов.

>>>

- Каждая версия API должна быть покрыта тестами, дабы гарантировать, что
  все работает так, как и работало, а формат запроса/выдачи не поменялся.

- Изменение схемы данных требует адаптации фейковых данных в тестах.

- По возможности не использовать `mock` при тестировании версий API.

>>>

```python
# Актуальный формат:
#
#   {'owner':
#        {'firstName': 'John',
#         'lastName': 'Doe'},
#    'product': some_product_data},
#
_database = [
    {'owner': 'John Doe',
     'product': some_product_data},
]

@mock.patch('project.database', _database)
def test_get_sales_v1(app):
    with app.test_client() as c:
        assert c.get('/v1/sales').json() == {
            'owner': 'John Doe',
            'product': some_product_data,
        }
```

---

### Эволюция бизнес-логики

- Разные версии API могут требовать разной версии бизнес-логики.

- Необходимо быть готовым к наличию нескольких альтернативных реализаций
  одной и той же функции.

- Следуя принципу DRY, очень легко оказаться в аду наследований,
  стратегий и сложных интерфейсов. Альтернатива – copy-paste подход.

>>>

```python
def assign_ips_lt_5_0(...):
    pass

def assign_ips_eq_5_0(...):
    pass

def assign_ips_gt_6_1(...):
    pass
```

---

### Выводы

Их нет. Каждый их должен сделать сам. :)

---

### Мои выводы

- Наличие нескольких версий API существенно увеличивает цену поддержки.

- Не поддерживать все множество существующих версий. Выбрать стратегию.
  Например, поддерживать последние `N` версий.

- Подумать об отказе от версионирования в случае закрытого продукта,
  если нет требований к обновлению с минимальным временем простоя.

>>>

- Использовать HTTP-заголовок для версионирования как самый простой
  и гибкий способ.

- Хранить тесты на каждую поддерживаемую версию API. Не использовать `mock`.

---

### Спасибо за внимание!

### Вопросы?
