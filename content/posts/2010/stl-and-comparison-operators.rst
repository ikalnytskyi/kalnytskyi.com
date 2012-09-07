=========================
STL и операторы сравнения
=========================

:author: Igor Kalnitsky
:date: 07.12.2010
:tags: cpp, stl
:slug: stl-and-comparison-operators


Не для кого не секрет, что STL не только предоставляет эффективную реализацию
стандартных алгоритмов/контейнеров, но и значительно сокращает время
разработки приложения.

В процессе моего изучения и освоения STL, мне удалось узнать об
предопределенных операторах сравнения, о существовании которых некоторые и не
предполагают. Эти операторы позволяют автоматически определить операторы
сравнения — ``<=``, ``>``, ``>=``, ``!=`` — для класса, перегрузив лишь
операторы ``==`` и ``<``. Находятся эти операторы в заголовочном файле
*utility* в пространстве имен *std::rel_ops*.

Ниже я привожу простой пример, демонстрирующий применение этих операторов.

.. code:: c++

    #ifndef _MYINT_HPP_
    #define _MYINT_HPP_

    #include <utility>
    using namespace std::rel_ops;

    class MyInt
    {
    public:
        MyInt(int x = 0);

        int value()const;

        bool operator==(const MyInt& rhs)const;
        bool operator<(const MyInt& rhs)const;

    private:
        int _x;
    };

    #endif // _MYINT_HPP_


.. code:: c++

    #include "myint.hpp"

    MyInt::MyInt(int x)
        : _x(x)
    {}

    int MyInt::value()const
    {
        return _x;
    }

    bool MyInt::operator==(const MyInt& rhs)const
    {
        return _x == rhs._x;
    }

    bool MyInt::operator<(const MyInt& rhs)const
    {
        return _x < rhs._x;
    }

При выполнении следующего кода:

.. code:: c++

    #include "myint.hpp"
    #include <iostream>

    void check(bool cmp);


    int main(int argc, char* argv[])
    {
        MyInt x1(5), x2(5), x3(8), x4(2);

        std::cout << "x1 = " << x1.value() << std::endl;
        std::cout << "x2 = " << x2.value() << std::endl;
        std::cout << "x3 = " << x3.value() << std::endl;
        std::cout << "x4 = " << x4.value() << std::endl;
        std::cout << "----------------------" << std::endl;

        // operator ==
        std::cout << "x1 == x2  |  "; check(x1 == x2);
        std::cout << "x1 == x3  |  "; check(x1 == x3);
        std::cout << "x1 == x4  |  "; check(x1 == x4);
        std::cout << std::endl;

        // operator <
        std::cout << "x1 <  x2  |  "; check(x1 < x2);
        std::cout << "x1 <  x3  |  "; check(x1 < x3);
        std::cout << "x1 <  x4  |  "; check(x1 < x4);
        std::cout << std::endl;

        // operator <=
        std::cout << "x1 <= x2  |  "; check(x1 <= x2);
        std::cout << "x1 <= x3  |  "; check(x1 <= x3);
        std::cout << "x1 <= x4  |  "; check(x1 <= x4);
        std::cout << std::endl;

        // operator >
        std::cout << "x1 >  x2  |  "; check(x1 > x2);
        std::cout << "x1 >  x3  |  "; check(x1 > x3);
        std::cout << "x1 >  x4  |  "; check(x1 > x4);
        std::cout << std::endl;

        // operator >=
        std::cout << "x1 >= x2  |  "; check(x1 >= x2);
        std::cout << "x1 >= x3  |  "; check(x1 >= x3);
        std::cout << "x1 >= x4  |  "; check(x1 >= x4);
        std::cout << std::endl;

        // operator !=
        std::cout << "x1 != x2  |  "; check(x1 != x2);
        std::cout << "x1 != x3  |  "; check(x1 != x3);
        std::cout << "x1 != x4  |  "; check(x1 != x4);

        return 0;
    }

    void check(bool cmp)
    {
        if (cmp)
            std::cout << "true" << std::endl;
        else
            std::cout << "false" << std::endl;
    }


Получим следующий результат:

.. code:: text

    x1 = 5
    x2 = 5
    x3 = 8
    x4 = 2
    ----------------------
    x1 == x2 | true
    x1 == x3 | false
    x1 == x4 | false

    x1 < x2 | false
    x1 < x3 | true
    x1 < x4 | false

    x1 <= x2 | true
    x1 <= x3 | true
    x1 <= x4 | false

    x1 > x2 | false
    x1 > x3 | false
    x1 > x4 | true

    x1 >= x2 | true
    x1 >= x3 | false
    x1 >= x4 | true

    x1 != x2 | false
    x1 != x3 | true
    x1 != x4 | true

Реализованы эти операторы примерно следующим образом.

.. code:: c++

    #ifndef UTILITY_
    #define UTILITY_

    namespace std
    {
        // шаблонная структура pair, входящая в <utility>,
        // а так же операторы для работы с ней

        namespace rel_ops
        {
            template<class t=""> inline
                bool operator!=(const T& X, const T& Y)
                {
                    return (!(X == Y));
                }

            template<class t=""> inline
                bool operator>(const T& X, const T& Y)
                {
                    return (Y < X);
                }

            template<class t=""> inline
                bool operator<=(const T& X, const T& Y)
                {
                    return (!(Y < X));
                }

            template<class t=""> inline
                bool operator>=(const T& X, const T& Y)
                {
                    return (!(X < Y));
                }
        }
    }

    #endif // UTILITY_

Конечно, для полной независимости собственного класса, можно написать и самому
операторы сравнения, тем более, что написать их несложно. Но данный пост
является больше познавательным, нежели поучающим хорошему тону программирования.
Кто знает, а вдруг именно операторы из **rel_ops** помогут вам в дальнейшем? :)
