===========================================================================
Introduction to C++11: nullptr and innovations of the initialization system
===========================================================================

:author: Igor Kalnitsky
:date: 04.09.2011
:tags: cpp
:slug: introduction-to-cpp11-part-2
:lang: en


As I promised, I continue writing about the new **C++** Standard. The
`previous post`_ was about:

- automatic type inference using ``auto``;
- type definition using ``decltype``;
- closing nested templates;
- ``range-based for`` loop.

No more, nor less than, I think. But readers understand that this is a tip of
an iceberg of features offered by new Standard.


nullptr
-------

C++11 got ``nullptr`` is a special keyword for nulling pointers. In the earlier
versions of Standard programmers should write:

.. code:: c++

    Foo* foo = 0;

Otherwise, they might use ``NULL`` macros, that comes from ``C``. But the
problem is obvious: *zero-based number* is used to null the pointer. That might
cause troubles, for example, while working with overloaded functions:

.. code:: c++

    void func(int x);
    void func(const Foo* ptr);
    // ...
    func(0);

Which function will be called? That's obvious, the first one as it has an
integer as an argument. And what if we want to call the another function that
have a nulled pointer as an argument? We'd need to use ``static_cast<>`` to
decide this problem.

.. code:: c++

    func(static_cast<const Foo*>(0));

But this problem is artificially. I must say, I've never been faced with it
within any project. But there is the real one. Let us suppose we have a
container consisting of pointers which we want to null. Knowing wonderful STL
algorithms we will use ``std::fill``.

.. code:: c++

    std::vector<Foo*> foos;
    // ...
    std::fill(foos.begin(), foos.end(), 0);

At first sight — everything is ok! But there is an error and it is similar
to the previous. ``std::fill`` is a template, and it assumes ``0`` as an
``int`` and, because of the type discrepancy we surely get a strange error
message from a compiler. The way out is to cast ``0`` to a pointer, but such
code doesn't increase code readability.

That's why ``nullptr`` keyword was accepted. And now we can avoid such
problems using this keyword as ``nullptr`` has it's own type —
``std::nullptr_t``.


Initializer lists
-----------------

The previous Standard the power of initialization lists was much lower. What
could we do earlier? Only just initialize some structure and some array:

.. code:: c++

    struct Struct
    {
        int x;
        std::string str;
    };

    // initialization of stucture attributes
    Struct s = { 4, "four" };

    // array initialization
    int arr[] = { 1, 8, 9, 2, 4 };

But C++ offers other, more comfortable and more flexible alternatives. I'm
talking about classes and containers. In C++11 such unfairness is finally
solved through the introduction of template class ``std::initializer_list<>``.
All containers posses a constructor taking an initializer list. So now such
code becomes possible:

.. code:: c++

    std::vector<int> v = { 1, 5, 6, 0, 9 };

It should be noticed that initialize lists are not always used to initialize.
For example, adding *few* elements to a container is now possible:

.. code:: c++

    std::vector<int> v;
    v.insert(v.end(), {0, 1, 2, 3, 4});

Developer can provide such possibility to his own class (in particular
container). He should just define constructor, taking
``std::initializer_list<>`` as an argument.

.. code:: c++

    class Foo
    {
    public:
        // ...
        Foo(std::initializer_list<int> list);
    };

    // ...
    Foo::Foo(std::initializer_list<int> list)
    {
        // do something
    }


    // ...
    int x = 5;
    Foo one = { 1, x, 2, 4, 8 };
    Foo two({ 5, 4, 2, x, 4 });

The ``std::initializer_list<>`` objects cannot be changed.


Uniform initialization
----------------------

Initializer lists — it's an amazing feature. But developers haven't stopped and
they've gone further. They extended the initializer lists syntax, allowing to
imagine such things:

.. code:: c++

    class Foo
    {
    public:
        // ...
        Foo(int x, double y, std::string z);
    };

    // ...
    Foo::Foo(int x, double y, std::string z)
    {
        // do something
    }

    // ...
    Foo one = { 1, 2.5, "one" };
    Foo two { 5, 3.14, "two" };

Such initialization will call constructor as if we write:

.. code:: c++

    Foo foo(1, 2.5, "one");

Uniform initialization works for both classes and structures. In case of
classes the constructor is called, and the elementwise initialization in the
order of attribute declaration is occurred for the structures.

.. code:: c++

    struct Foo
    {
        std::string str;
        double x;
        int y;
    };

    Foo foo {"C++11", 4.0, 42}; // {str, x, y}
    Foo bar {"C++11", 4.0};     // {str, x}, y = 0

If the last attribute(s) isn't specified than default constructor is called.
For embedded types such as ``int`` null initialiation will be occurred. It is
worth noting that such initialization allows to write such stuff:

.. code:: c++

    Foo getFoo()
    {
        return { 5, 3.14, "hello" };
    }

    int* foo = new int[5]{0, 1, 2, 3, 4};

It is interesting to know that uniform initialization protects from implicit
conversions.

.. code:: c++

    class Foo
    {
    public:
        Foo(int x): _x(x) {}

    private:
        int _x;
    };
    // ...
    Foo foo(3.14);  // ok, double -> int
    Foo bar{3.14};  // error!

After becoming acquainted with uniform initialization You might have question:
*"What constructor is called in this case?"*.

.. code:: c++

    class Foo
    {
    public:
        Foo(int x, int y) {}
        Foo(std::initializer_list<int> list) {}
    };

    Foo foo(1, 2);
    Foo bar{1, 2};

In this case constructor ``Foo(int x, int y)`` is called to create ``foo``, and
``Foo(std::initializer_list<int> list)`` to create ``bar``. In case of the last
constructor is absent all the objects are initialized by the
``Foo(int x, int y)``.


Instead of conclusion
---------------------

I wish to write a lot but got just a little bit. It is a problem to pick out
some time for writing. Well, I described the most general features
(except for lambdas). Later on I'll write about some particular features.

.. _previous post: /2011/08/28/introduction-to-cpp11-part-1/en/
