==========
listbox.js
==========

:slug: projects/listbox.js
:lang: en


.. image:: /static/images/projects/listbox.js/listbox.js.png
    :alt: listbox.js screenshot
    :align: right
    :height: 270px

**Listbox.js** is a simple jQuery_ plugin that provides a more powerful
alternative to the standard ``<select>`` tag. The main problem of ``<select>``
tag is that last one isn't flexible for customization with CSS.

Listbox.js solves this problem. This component runs on top of ``<select>``
tag and creates an alternative to the last one based on ``<div>`` tags.
It opens up great possibilities for customization.

In addition, this component provides the search bar which
would be useful in lists with a lot of items.

`Source code is available on Github <https://github.com/ikalnitsky/listbox.js>`_


Usage
-----

Link the component and a stylesheet from your page.

.. code:: html

    <!-- jQuery should be already included -->
    <link href="styles/jquery.listbox.css" rel="stylesheet">
    <script src="js/jquery.listbox.js"></script>


Call ``listbox()`` method for necessary ``<select>`` tags.

.. code:: html

    <script>
      $(function() {
        $('select').listbox({
          'class':        'myOwnClass',   // this class would be added to the list
          'searchbar':    true,           // show search bar
          'multiselect':  false           // don't use multiselect list
        })
      })
    </script>


Customization
-------------

For appearance customization you should use the following CSS classes.

.. code:: css

    /* <div>: component container */
    .lbjs {}

    /* <div>: container for the list items */
    .lbjs-list {}

    /* <div>: list item */
    .lbjs-item {}

    /* <div>: disabled list item */
    .lbjs-item[disabled] {}

    /* <input>: search query input box */
    .lbjs-searchbar {}


.. _jQuery: http://jquery.com/
.. _XSnippet: http://xsnippet.org/
