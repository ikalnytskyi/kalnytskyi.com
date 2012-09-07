=================================
Пользовательские литералы в C++11
=================================

:author: Igor Kalnitsky
:date: 20.03.2012
:tags: cpp
:slug: user-defined-literals-in-cpp11


Более полугода прошло с момента принятия стандарта C++11. В сети можно найти
много материалов посвященных новому стандарту, однако большинство из них
касаются самых простых возможностей, самых сладких. Я говорю о лямбда-функциях,
системе автоматического выведения типов, новых спецификаторах, умных
указателях и т.д. Да, это действительно интересные вещи и, можно смело сказать,
они одни из самых полезных и часто используемых. Но на них свет клином не
сошелся, и новенький C++11 предлагает нам не только их.

Ниже я хочу рассказать о пользовательских литералах — весьма полезном
средстве, хоть и не в повседневных целях.


Что такое литерал?
------------------

**Литерал** — это некоторое выражение, создающее объект. Литералы появились
не только в C++11, они были и в C++03. Например, есть литералы для создания
символа, строки, вещественных чисел, и т.д.

.. code:: c++

    'x';      // character
    "some";   // c-style string
    7.2f;     // float
    74u;      // unsigned int
    74l;      // long
    0xF8;     // hexadecimal number

Все это литералы. С понятием литералов мы разобрались. Самое время вернуться
к C++11.


Пользовательские литералы в C++11
---------------------------------

Как уже было отмечено выше, новый стандарт предлагает средства для создания
пользовательских литералов. Существует две категории пользовательских
литералов: *сырые литералы (raw)* и *литералы для встроенных типов (cooked)*.

Стоит, однако, заметить, что C++ позволяет создавать только литералы-суфиксы.
Иными словами, создать литералы префиксы (как, например, ``0x``), или
префиксо-суфиксные (как ``""``) — не получится.


Литералы для численных типов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Начнем с литералов для встроенных типов. Чтобы создать литерал для численных
типов необходимо воспользоваться одной из двух сигнатур:

.. code:: c++

    // сигнатура литерала для целочисленных типов
    OutputType operator "" _suffix(unsigned long long);

    // сигнатура литерала для вещественных типов
    OutputType operator "" _suffix(long double);

Использование литерала будет осуществляться следующим образом:

.. code:: c++

    42_suffix;      // OutputType operator "" _suffix(unsigned long long);
    42.24_suffix;   // OutputType operator "" _suffix(long double);

Обратите внимание на сигнатуры:

- литерал для целых чисел в качестве аргумента принимает ``unsigned long long``
- литерал для вещественных чисел в качестве аргумента принимает ``long double``

Данные типы взяты неспроста и их нельзя заменить на другие. Они являются
**обязательными** и утверждены стандартом языка.

Ниже приведен пример литерала, преобразовывающего минуты в секунды.

.. code:: c++

    unsigned long long operator "" _min(unsigned long long minutes)
    {
        return minutes * 60;
    }

    // ...

    std::cout << 5_min << std::endl; // на экран выведется 300


Литералы для строковых типов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Для создания литерала этого типа, необходимо воспользоваться одной из следующих
сигнатур:

.. code:: c++

    OutputType operator "" _suffix(const char* str, size_t size);
    OutputType operator "" _suffix(const wchar_t* str, size_t size);
    OutputType operator "" _suffix(const char16_t* str, size_t size);
    OutputType operator "" _suffix(const char32_t* str, size_t size);

Сигнатура выбирается в зависимости от типа строки:

.. code:: c++

    "1234"_suffix;   // operator "" _suffix(const char* str, size_t size);
    u8"1234"_suffix; // operator "" _suffix(const char* str, size_t size);
    L"1234"_suffix;  // operator "" _suffix(const wchar_t* str, size_t size);
    u"1234"_suffix;  // operator "" _suffix(const char16_t* str, size_t size);
    U"1234"_suffix;  // operator "" _suffix(const char32_t* str, size_t size);

Пример литерала преобразующего C-style строку в ``std::string`` приведен ниже.

.. code:: c++

    std::string operator "" s(const char* str, size_t size)
    {
        return std::string(str, size);
    }

    // ...

    std::cout << "some string"s.length() << std::endl;



Сырые литералы
~~~~~~~~~~~~~~

Ну и наконец настало время сырого литерала. Сигнатура сырого литерала выглядит
следующим образом:

.. code:: c++

    OutputType operator "" _suffix(const char* literalString);


Этот тип литералов приходит на помощь тогда, когда входное число надо
разобрать посимвольно. То есть, в этом случае число передает в оператор
как строка. Если не совсем понятно, взгляните на приведенный ниже код:

.. code:: c++

    OutputType operator "" _x(unsigned long long);
    OutputType operator "" _y(const char*);

    1234_x;     // call: operator "" _x(1234);
    1234_y;     // call: operator "" _y("1234");

Используя данный тип литералов можно написать литерал, преобразующий двоичное
число в десятичное. Например вот так:

.. code:: c++

    unsigned long long operator "" _b(const char* str)
    {
        unsigned long long result = 0;
        size_t size = strlen(str);

        for (size_t i = 0; i < size; ++i)
        {
            assert(str[i] == '1' || str[i] == '0');
            result |= (str[i] - '0') << (size - i - 1);
        }

        return result;
    }

    // ...

    std::cout << 101100_b << std::endl; // выведет 44

Существует еще одна сигнатура для сырых литералов. Основана она на применении
*Variadic Template*:

.. code:: c++

    template <char...>
        OutputType operator "" _b()

Преимущества литералов на базе *Variadic Template* заключается в том, что они
могут вычисляться на этапе компиляции. Тот же литерал преобразования двоичного
числа в десятичное может быть переписан так:

.. code:: c++

    template <char... bits>
        struct to_binary;

    template <char high_bit, char... bits>
        struct to_binary<high_bit, bits...>
        {
            static_assert(high_bit == '0' || high_bit == '1', "Not a binary value!");
            static const unsigned long long value =
                (high_bit - '0') << (sizeof...(bits)) | to_binary<bits...>::value;
        };

    template <char high_bit>
        struct to_binary<high_bit>
        {
            static_assert(high_bit == '0' || high_bit == '1', "Not a binary value!");
            static const unsigned long long value = (high_bit - '0');
        };

    template <char... bits>
        constexpr unsigned long long operator "" _b()
        {
            return to_binary<bits...>::value;
        }

    // ...

    int arr[1010_b]; // значение вычисляется compile-time
    std::cout << 101100_b << std::endl; // выведет 44


У внимательно читателя мог возникнуть вопрос: *"А что если создать и сырой
литерал, и литерал для числа с одним и тем же именем? Какой литерал
компилятор применит?"*. Стандарт по этому поводу дает точный ответ и
говорит о попытке компилятора применить литералы в следующем порядке:

* ``operator "" _x (unsigned long long)`` или ``operator "" _x (long double)``
* ``operator "" _x (const char* raw)``
* ``operator "" _x <'c1', 'c2', ... 'cn'>``

Полезно знать, что если определенный пользователем литерал совпадает с
системным (например ``f``), то выполнится системный.

.. code:: c++

    long operator "" f(long double value)
    {
        return long(value);
    }
    // ...
    std::cout << 42.7f << std::endl; // выведет 42.7


Вместо заключения
-----------------

**Бьёрн Страуструп** на конференции *Going Native 2012* приводил полезный
пример использования литералов. Мне кажется, он наглядно демонстрирует
факт повышения читаемости кода, а также снижает вероятность ошибиться.

.. code:: c++

    Speed sp1 = 100m / 9.8s;    // very fast for a human
    Speed sp2 = 100m / 9.8s2;   // error (m/s2 is acceleration)
    Speed sp3 =  100 / 9.8s;    // error (speed is m/s and 100 has no unit)

Механизм пользовательских литералов — это полезный **в некоторых**
случаях инструмент. Использовать его где попало не стоит. Подумайте дважды,
прежде чем их использовать, ведь литералы коварны: они могут..

* как повысить читаемость кода, так и понизить;
* как сыграть вам на руку, так и против вас.

**p.s.**
Пользовательские литералы поддерживаются компиляторами *gcc 4.7* и *clang 3.1*.
