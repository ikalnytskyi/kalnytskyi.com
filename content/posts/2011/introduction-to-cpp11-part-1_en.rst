===========================================================================
Introduction to C++11: auto, decltype, nested templates and range-based-for
===========================================================================

:author: Igor Kalnitsky
:date: 28.08.2011
:tags: cpp
:slug: introduction-to-cpp11-part-1
:lang: en


This post starts a new set of publications about the innovations of C++11
standard, which was approved not so long time ago. The most important and
simple innovations are considered below in this text. In the following posts
we will go deeper.


Type declaration using auto
---------------------------

Looking back in the history, we must point out that **auto** variables existed
earlier, before the approving of C++11 standard. But their meaning was
different. ``auto`` considered as a variable storing specificator. That means
``auto`` was like ``register``, ``static`` and ``extern``, and indicated that
variable had local life time. Most of the beginners doesn't know about that,
as every variable declared within certain block is estimated ``auto`` by
default.

For example two following listings are equal:

.. code:: c++

    void foo()
    {
        auto int x = 0;  // `auto` is indicated explicitly
        int y = 0;       // `auto` is indicated implicitly
    }

C++11 standard declares new meaning to this keyword, which I estimate more
useful than it was. From this time ``auto`` allows skipping type declaration
explicitly. The compiler will do it for you. It determines the type based
on the type of expression is initialized.

.. code:: c++

    void foo()
    {
        auto x = 5;  // th type of x is int
        x = "foo";   // error! type mismatch

        auto y = 4, z = 3.14; // error! different type variables are not allowed
    }

With brining ``auto`` into service the code readability increases considerably!
You no longer have to write long and complicated template types. E.g. to get
iterator:

.. code:: c++

    // c++03
    for (std::vector<std::map<int, std::string>>::const_iterator it = container.begin();
         it != container.end();
         ++it)
    {
        // do something
    }

    // c++11
    for (auto it = container.begin(); it != container.end(); ++it)
    {
        // do something
    }


What is decltype and what is it for?
------------------------------------

**decltype** allows to statically determine the type using the other variable
type.

.. code:: c++

    int x = 5;
    double y = 5.1;

    decltype(x) foo;    // int
    decltype(y) bar;    // double

    decltype(x+y) baz;  // double

Pay attention to the last line. Type could be even defined based on
calculation of mathematic expressions under variables. This is very useful
and powerful facility used to specify the return type of template functions.
However, the code with ``decltype`` is read not so easy, as we would want.

.. code:: c++

    template<class T, class U>
        auto hellSum(const T& x, const U& y) -> decltype(x + y)
        {
            return x + y;
        }

This is only example, actually ``decltype`` might be used to get the result of
functions, functors etc.


>> as an operation to close nested template
-------------------------------------------

The problem of closing comlicated template types have existed since the first
standard. The idea behind was that two signs ``>`` could not be written
together like ``>>``. Maybe it is due to the fact that sometime writing a
smart parser which recognize ``>>`` depending on the context was a huge problem.

.. note:: Note: ``>>`` is also a shift to the right. Furthermore, such
    verification was too high-priced (when we talk about performance).

Anyway, we had the following:

.. code:: c++

    std::vector<std::map<int, int>> foo;    // error
    std::vector<std::map<int, int> > foo;   // ok

But the approving C++11 standard made the first variant is legal and correct.


Range-Based for
---------------

**Range-Based for** is a cycle going through container. It is similar to
``for each`` in Java or C#. Syntactically it replicates ``for each`` in Java.
It is primarily called ``Range-Based`` to avoid the jumble, because STL has
already have an algorithm called ``std::for_each``.

.. code:: c++

    std::vector<int> foo;

    // fill foo

    for (int x : foo)
        std::cout << x << std::endl;

References works as well as elsewhere

.. code:: c++

    for (int& x : foo)
        x *= 2;

    for (const int& x : foo)
        std::cout << x << std::endl;

The code is pretty and easy, isn't it? ``auto`` which is discussed above
increases this construction.

.. code:: c++

    std::vector<std::pair<int, std::string>> container;

    // ...

    for (const auto& i : container)
        std::cout << i.second << std::endl;

``Range-based for`` implicitly calls methods ``begin()`` and ``end()`` of the
container and they foremost return iterators.

By the way, Range-Based for works with usual static arrays:

.. code:: c++

    int foo[] = {1, 4, 6, 7, 8};

    for (int x : foo)
        std::cout << x << std::endl;


Instead of conclusion
---------------------

Only a few innovations of C++11 standard were given above. There are much more
interesting things, and you will know about them later on. All you need is
to get the subscribe to my blog. :)
