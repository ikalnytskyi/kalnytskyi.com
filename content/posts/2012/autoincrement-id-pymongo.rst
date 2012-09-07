======================================
Добавление автоинкремента id в PyMongo
======================================

:author: Igor Kalnitsky
:date: 07.08.2012
:tags: python, mongodb
:slug: autoincrement-id-pymongo

.. image:: /static/images/2012/logo-mongodb.png
    :alt: MongoDB logotype
    :align: left

Не так давно отцами-основателями сервиса XSnippet_ было решено переписать его
с применением микрофреймворка Flask_ (об этом я писал в своём `твиттере`_).
Основная причина этого решения заключается в желании изучить новые технологии
и реализовать полноценное *RESTful API*.

Для хранения данных было решено использовать популярные ныне NoSQL
базы данных, а именно — MongoDB_.

**MongoDB** — это хорошо масштабируемая и высокопроизводительная база данных,
обладающая рядом преимуществ:

* документо-ориентированное хранилище (простая и мощная JSON-подобная схема);
* динамические запросы;
* быстрое обновление данных;
* поддержка индексов;
* нет надобности в ORM;
* удобная работа из Python (``dict`` является представлением JSON-документа);
* многое другое.

Для работы с MongoDB из Python существует библиотека PyMongo.


Ложка дёгтя
-----------

Однако, без ложки дёгтя не обойдешься. При сохранении документа в MongoDB,
ему присваивает уникальный идентификатор ``_id``. MongoDB генерирует сложный
и неудобный идентификатор (о его формате можно почитать на `сайте MongoDB`_).

Разумеется, в большинстве случаев нам не важно как выглядит идентификатор,
но в случае с XSnippet_ — это весьма существенно. И тогда я задался вопросом:
как реализовать **автоинкрементный идентификатор** на MongoDB?


Счетчики
--------

В процессе недолгого поиска в Интернете, *нормального* решения найдено не
было. Везде предлагался один и тот же вариант:

* завести отдельную коллекцию со счетчиками (последними ``_id``);
* получать это значение, инкрементировать и явно указывать в качестве ``_id``
  при добавлении нового элемента.

То есть предлагалось нечто следующее.

.. code:: python

    def get_next_id(collection_name):
        result = db.counters.find_and_modify(query={"_id": collection_name},
                                             update={"$inc": {"next": 1}},
                                             upsert=True, new=True)
        return result["next"]

    # somewhere else
    db.snippets.insert({"_id": get_next_id("snippets"), "title": "Test"})

Но это решение мне не понравилось. Да, его можно практиковать и это будет
работать, но оно не элегантное с точки зрения пользовательского кода.
Нас принуждают самим указывать ``_id`` и *ключ* записи хранящий нужный ``_id``.
С таким подходом легко запутаться и внести ошибки в код.


Манипуляторы
------------

Поэтому сегодня утром я решил поизучать код библиотеки ``PyMongo``, и,
возможно, внести в него правки для нормальной работы со своими генераторами
идентификаторов. В процессе исследования было обнаружено, что прежде чем
выполнять вставку (добавление) элемента в базу данных, они все проходят
через так называемые *манипуляторы*. Более того, класс базы данных
поддерживает регистрирование пользовательских манипуляторов.

Исходя из этого мною был написан небольшой класс-манипулятор, задача которого
состоит в том, чтобы симулировать автоинкрементный ``_id``. Работает класс
просто: проверяет наличие ``_id`` во входящем документе и, в случае его
отсутствия, добавляет с правильным автоинкрементым значением.

Сам манипулятор выглядит так.

.. code:: python

    from pymongo.son_manipulator import SONManipulator


    class AutoincrementId(SONManipulator):
        """A son manipulator that adds the autoincrement ``_id`` field.

        Adding only occurs if ``_id`` missing in son object.

        Usage example::

            db.add_son_manipulator(AutoincrementId())
        """

        def transform_incoming(self, son, collection):
            """Add an ``_id`` field if it's missing.

            :param son: a son object (document object)
            :param collection: a collection for inserting
            """
            if "_id" not in son:
                son["_id"] = self._get_next_id(collection)
            return son

        def _get_next_id(self, collection):
            """Retrieve an id for inserting into a certain collection.

            :param collection: a collection for inserting
            """
            database = collection.database
            result = database._autoincrement_ids.find_and_modify(
                         query={"_id": collection.name,},
                         update={"$inc": {"next": 1},},
                         upsert=True,  # insert if object doesn’t exist
                         new=True,     # return updated rather than original object
                     )
            return result["next"]


Регистрация манипулятора происходит следующим образом.

.. code:: python

    # make connection and select database
    connection = Connection()
    db = connection.test_db

    # use autoincrement id
    db.add_son_manipulator(AutoincrementId())


После чего любой добавляемый документ получит правильный автоинкрементный
``_id``, без необходимости указания его (``_id``) вручную.


.. _XSnippet: http://www.xsnippet.org/
.. _Flask: http://flask.pocoo.org/
.. _твиттере: https://twitter.com/ikalnitsky/status/231338489042571265
.. _MongoDB: http://www.mongodb.org/
.. _сайте MongoDB: http://www.mongodb.org/display/DOCS/Object+IDs
