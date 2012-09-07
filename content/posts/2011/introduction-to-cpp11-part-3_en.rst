=========================================
Introduction to C++11: lambda expressions
=========================================

:author: Igor Kalnitsky
:date: 30.10.2011
:tags: cpp
:slug: introduction-to-cpp11-part-3
:lang: en


In previous posts I familiarized you with some interesting features of the
new C++11 Standard. Today I continue the diving and tell about *lambda
expressions*.

The C++11 Standard finally provided such useful thing as lambda expressions.
Advanced C++ developer will exclaim: *"But lambda are already exist in
boost!"*. That's right. But the new lambda are more powerful and, at my humble
opinion, more practical. However I'm not going to compare realization of these
lambdas. My point is to tell what is lambda and what it is used for.

Without getting into the origins of appearance of lambdas, I tell, that lambda
is a shorter form of functor. Some kind of nameless functor. Consider the
following example.

Suppose we have some integer vector. The task is to sort the items so that
elements on the left were odd, and on the right — even. To accomplish this, we
need to write a functor and pass it to ``std::sort``.

.. code:: c++

    struct Comparator : public std::binary_function<int, int, bool>
    {
        bool operator()(int lhs, int rhs)const
        {
            if (lhs & 1  &&  rhs & 1)
                return lhs < rhs;
            return lhs & 1;
        }
    };

    std::sort(vec.begin(), vec.end(), Comparator());

Writing a functor is an easy task, but, anyway we write too much code and code
readability goes lower. Writing a whole functor class just to use it once
isn't the best design. So here we can use the lambda functions. With their
help the above written code can be written as:

.. code:: c++

    std::sort(vec.begin(), vec.end(), [](int lhs, int rhs) -> bool {
        if (lhs & 1  &&  rhs & 1)
            return lhs < rhs;
        return lhs & 1;
    });

This form is more illustrative and more compact. But let me consider the
syntax in detail. In general, it can be written as:

.. code:: c++

    [captures](arg1, arg2) -> result_type { /* code */ }

``arg1``, ``arg2``
    are arguments, i.e. that is passed by the algorithm to the functor(lambda)

``result_type``
    is a type of return value. It may seem a bit unusual, because before the
    type was always written before the entity (variable, function). But you
    get used to it quickly.

    .. note:: It is worth noting that if lambda consists only of the ``return``
        operator, the type might not be specified. E.g:

        .. code:: c++

            std::sort(vec.begin(), vec.end(), [](int lhs, int rhs) {
                return lhs & 1;
            });

Now let's talk about the ``captures``. Captures define the environment
variables that should be available within the lambda. These variables can be
captured by value or by reference.

.. code:: c++

    int max = 4;

    // by value
    std::sort(vec.begin(), vec.end(), [max](int lhs, int rhs) {
        return lhs < max;
    });
    // by reference
    std::sort(vec.begin(), vec.end(), [&max](int lhs, int rhs) {
        return lhs < max;
    });

Also, you can capture all the variables out of scope:

.. code:: c++

    // by value
    std::sort(vec.begin(), vec.end(), [=](int lhs, int rhs) {
        return lhs < someVar;
    });

    // by reference
    std::sort(vec.begin(), vec.end(), [&](int lhs, int rhs) {
        return lhs < otherVar;
    });

Lambda as well as the functors, can be passed to the function and they are
easily assigned to variables.

.. code:: c++

    auto square = [](int x) { return x * x; };
    std::cout << square(16) << std::endl;

If lambda is created in a certain class method and it is necessary address
from it to a certain attribute, then the capture of this attribute does not
work. In order to to address to any attribute/method, it is necessary to
capture ``this``. At the same time it's not necessary to put ``this`` in the
lambda body before the attribute/method.

.. code:: c++

    class Foo
    {
    public:
        Foo(): _x(5) {}

        void doSomething() {
            // если вместо this поставить _x — будет ошибка!
            auto lambda = [this](int x) {
                std::cout << _x * x << std::endl;
            };

            lambda(4);
        }

    private:
        int _x;
    };
