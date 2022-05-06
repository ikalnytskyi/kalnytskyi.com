---
summary: >-
  In this essay I share my thoughts on C, its legacy and relations with C++.
aliases: /2014/10/25/c-legacy-is-evil/
---

C Legacy Is 😈 Evil
===================

When people ask me what is the most annoying thing in C++ in my opinion, I
answer without hesitation that it's C legacy. I keep choosing C legacy even
among dozens other nasty things C++ posses. So what meaning do I put into these
words? Well, I put everything that doesn't fit into C++ ideology and has been
kept in the language for backward compatibility reasons. What a great advantage
it was years ago, and what unpleasant drawback it is today.

When I was working at [Gameloft], I was involved into [Blitz Brigade]
development. At some point the decision had been made to revive the Android
port and I was helping the Android team to make it happen.

One day I was asked to assist them with troubleshooting a mysterious
server-client communication issue. The client part, that was running on an
Android device, has been rejected by the server. The Android port was nothing
more but a Java shim around the game written in C++, and so the team had no
experience with C++. PDigging into the code I've discovered a widespread,
typical mistake often occurred in the C world. What was strange is that the
issue has never been found on iOS and had nearly 100% repro rate on Android.

So what was that? Let's look at the following code snippet that converts a
datetime object into a Unix timestamp:

```cpp
// year, month, day, hour, min and sec are retrieved via network
// and have valid values

struct tm tm_struct;

tm_struct.tm_year = year - 1900;
tm_struct.tm_mon = month - 1;
tm_struct.tm_mday = day;

tm_struct.tm_hour = hour;
tm_struct.tm_min = min;
tm_struct.tm_sec = sec;

tm_struct.tm_wday = 0;
tm_struct.tm_yday = 0;

time_t time = std::mktime(&tm_struct);
```

At first glance, there's nothing wrong here, yet `time` was `0` on Android and
a valid timestamp on iOS. Experienced C programmers know that structures must
be `memset`-ed before being used, otherwise one or more explicitly
uninitialized fields may contain garbage. `tm_struct` is no exception, but the
following lines were missing in the code:

```cpp
struct tm tm_struct;
memset(&tm_struct, 0, sizeof(tm_struct));
```

It turned out that there's one more field in `tm_struct`: `tm_isdst`. It's easy
to miss because daylight saving time is easy to forget about. According to C
memory model, uninitialized fields or variables may or may not contain garbage.
This garbage consequently lead to the fact that `std::mktime` returned `0`. I
had no time to investigate why there were no garbage in case of iOS build, but
my gut tells me that the reason lied in compiler's configuration.

Now why am I blaming C legacy here? Well, first and foremost because in C++
world we have constructors and it's common for structures and claases to
initialize its fields upon constructions. No one wants garbage there, pretty
much everybody would prefer to see zeroes. `tm_struct` is a structure that
comes from C and has no implemented constructor, and therefore must be
`memset`-ed manually.

The huge problem I see here is that there's no way to differentiate C
structures from C++ ones. Programmers MUST remember what is what in order to
prevent such bugs. This is so wrong and confusing, not saying that programmers
have better things to occupy their minds. Issues such as this should not exist
in the first place. Even if a backward compatibility with C was very much
desired, a well designed language should have provided at least some measures
to prevent programmers falling into a rabbit hole.

[Gameloft]: http://www.gameloft.com/
[Blitz Brigade]: https://itunes.apple.com/us/app/blitz-brigade-online-multiplayer/id580175049?mt=8
