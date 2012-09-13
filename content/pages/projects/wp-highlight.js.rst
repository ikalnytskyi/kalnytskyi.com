===============
wp-highlight.js
===============

:slug: projects/wp-highlight.js


.. image:: /static/images/projects/wp-highlight.js/wp-highlight.js.png
    :alt: wp-highlight.js screenshot
    :align: right
    :height: 270px

.. warning:: На данный момент плагин более не поддерживается. Но вы можете
    легко обновить его ядро, просто заменив файл ``highlight.pack.js``
    в каталоге с плагином. Последню версию ``highlight.pack.js`` можно взять
    на `официальном сайте`_.

    .. _`официальном сайте`: http://softwaremaniacs.org/soft/highlight/download/

**wp-highlight.js** — это простой Wordpress_-плагин для highlight.js_.
Highlight.js — это JavaScript библиотека для подсветки кода на блогах, форумах
и вообще на любых веб-страницах. Библиотека проста в использовании, так как
работает автоматически: находит блоки кода, определяет язык и подсвечивает код.

`Исходный код доступен на GitHub <https://github.com/ikalnitsky/wp-highlight.js>`_


Особенности
-----------

* работает с комментариями
* высокопроизводительна
* красивые цветовые темы


Установка
---------

#. Загрузите ``wp-highlight.js`` в каталог ``/wp-content/plugins/``.
#. Активируйте плагин на странице «Плагины» в админке WordPress.
#. Используйте конструкцию вида ``[code lang="some_lang"]some code[/code]``
   для подсветки кода с указанием языка или же ``[code]some code[/code]``
   для подсветки кода с автораспознованием языка. Вы также можете использовать
   html-теги ``<pre><code>`` вместое bb-кода ``[code]``

.. _Wordpress:      http://wordpress.org/
.. _highlight.js:   http://softwaremaniacs.org/soft/highlight/
