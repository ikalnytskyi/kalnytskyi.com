---
summary: >-
  Docker, Python and how to use them together in daily routine, like running
  unit tests.
aliases: /2015/02/03/docker-for-pythonistas/
---

Docker For Pythonistas
======================

[Docker]'s popularity is growing day by day and every last man wrote about
it. Well, I'm a slowpoke... so sorry if I wrote something you already know.
Anyway, if you're already familiar with Docker I'm not sure if that makes
sense for you to waste time and read this post; otherwise - you're welcome.

My acquaintance with Docker began almost a year ago, when we decided to use
it as an upgrade mechanism in [Fuel for OpenStack]. For sure I learned a lot
about Docker since that time: I know about its limitations, pitfalls and
bugs; I even know how to run the latest version (v1.4.1) on CentOS 6.5 with
old Linux kernel.

In this post I'm not going to tell you about all possible use cases for
Docker or about its internals and limitations. Instead, I'll try to focus on
the daily usage flow and why I found it useful for myself and why it might
be useful for Pythonistas in general.

I’ll try to be straight to the point, but before we go further let's answer
the following questions:

 * What is the most common "action" for programmers?
 * What is the second most common "action" for programmers?

Well, obviously, an answer to the first question is *to write code*.
Programmers are supposed to write code, they're doing it almost every day
and it takes a lot of their time.

And what about the second question? The answer is *to run tests* in order to
be sure that nothing is broken. Unfortunately, it may not be as easy as it
seems. You know, a lot of Python software is supposed to be run on various
Python interpreters: it may be a set of Py2 interpreters or even both Py2
and Py3 interpreters. So for proper testing the tests should be run against
a certain set of Python interpreters, but what to do if some of them are
unavailable for your Linux distributive?

This is where Docker is going to help us.

Docker is a platform for building, shipping and running containers. In other
words it allows you to prepare an image with some software, push it to
docker registry (sort of repository) and pull it wherever you want to run.

I came to it when I needed to run tests against Python 2.6 and this
interpreter wasn't available for Debian Jessie. So I spent some time and
built a [pythonista docker image] that contained the most popular Python
interpreters. It's very convenient since anyone can pull this image and use
it to run tests. If you aren't satisfied by my image, you can always build
your own - it's not a challenge.

Tests could be run in the container with just a single command, no
pre-configuration is required, but pull the image. The whole workflow could
look like:

```bash
$ docker pull ikalnitsky/pythonista
$ docker run -v /path/to/src/:/src -w /src ikalnitsky/pythonista tox
```

For those who aren't familiar with Docker, the first command retrieves the
image from the Docker registry and the second one runs a container created
from it. The arguments are

 * `-v /path/to/src:/src` - mounts `/path/to/src` from your host machine
   into `/src` inside your container
 * `-w /src` - change current working directory inside container to `/src`
 * `ikalnitsky/pythonista` - obviously, use this image for container
 * `tox` - run tox (a test runner tool)

So why Docker? What does it bring to you? It saves your time and nerves
because you don't need to compile missed Python interpreters on every
machine you're working on. Still, this is one of possible Docker use cases,
so don't hesitate to find your own.


[Docker]: https://www.docker.com
[Fuel for OpenStack]: https://wiki.openstack.org/wiki/Fuel
[pythonista docker image]: https://github.com/ikalnitsky/pythonista
