===============
wp-highlight.js
===============

:slug: projects/wp-highlight.js
:lang: en


.. image:: /static/images/projects/wp-highlight.js/wp-highlight.js.png
    :alt: wp-highlight.js screenshot
    :align: right
    :height: 270px

.. warning:: This plugin doesn't supported now. But you can easy update
    ``highligh.js`` core by replacing ``highlight.pack.js`` in plugin
    directory. The latest version of ``highlight.pack.js`` you can get
    from `official site`_.

    .. _`official site`: http://softwaremaniacs.org/soft/highlight/en/download/


**wp-highlight.js** is a simple Wordpress_ plugin for highlight.js_ library.
Highlight.js highlights syntax in code examples on blogs, forums and in fact
on any web pages. It's very easy to use because it works automatically:
finds blocks of code, detects a language, highlights it.

`Source code is available on Github <https://github.com/ikalnitsky/wp-highlight.js>`_


Features
--------

* works with comments
* high performance
* nice colorshemes


Installation
------------

#. Upload ``wp-highlight.js`` to the ``/wp-content/plugins/`` directory.
#. Activate the plugin through the «Plugins» menu in WordPress admin page.
#. Use ``[code lang="some_lang"]some code[/code]`` construction for
   highlighting specified language or ``[code]some code[/code]`` for
   highlighting with language autodetection. You also can use ``<pre><code>``
   tags instead ``[code]`` bb-tag.


.. _Wordpress:      http://wordpress.org/
.. _highlight.js:   http://softwaremaniacs.org/soft/highlight/en/
