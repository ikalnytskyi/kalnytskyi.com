==========
listbox.js
==========

:slug: projects/listbox.js


.. image:: /static/images/projects/listbox.js/listbox.js.png
    :alt: listbox.js screenshot
    :align: right
    :height: 270px

**Listbox.js** — это простой jQuery_-плагин, предоставляющий альтернативу
стандартному ``html``-тегу ``<select>``. Основная проблема стандартной
(браузерной) реализации тега ``<select>`` заключается в том, что нельзя
изменить его внешний вид при помощи CSS.

Listbox.js предлагает альтернативу. Он работает поверх существующего
тега ``<select>``, заменяя браузерную реализацию, реализацией основанной на
``<div>`` верстке, что позволяет гибко настроить его внешний вид при помощи
CSS.

В дополнение ко всему, данный компонент предоставляет *строку поиска*,
которая позволяет облегчить выбор нужного элемента в большом списке.

`Исходный код доступен на GitHub <https://github.com/ikalnitsky/listbox.js>`_


Использование
-------------

Подключите файлы плагина:

.. code:: html

    <!-- jQuery должен быть уже подключен -->
    <link href="styles/jquery.listbox.css" rel="stylesheet">
    <script src="js/jquery.listbox.js"></script>


Вызовите метод ``listbox()`` у нужных ``<select>`` тегов.

.. code:: html

    <script>
      $(function() {
        $('select').listbox({
          'class':        'myOwnClass',   // класс, который будет добавлен
          'searchbar':    true,           // отображать строку поиска
          'multiselect':  false           // не использовать множественный выбор
        })
      })
    </script>


Настройка стилей
----------------

Для настройки внешнего вида, необходимо использовать следующие CSS-классы.

.. code:: css

    /* <div>: контейнер компонента */
    .lbjs {}

    /* <div>: контейнер для списка */
    .lbjs-list {}

    /* <div>: элемент списка */
    .lbjs-item {}

    /* <div>: disabled элемент списка */
    .lbjs-item[disabled] {}

    /* <input>: строка поиска */
    .lbjs-searchbar {}


.. _jQuery: http://jquery.com/
.. _XSnippet: http://xsnippet.org/
