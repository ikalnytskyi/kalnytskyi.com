---
summary: >-
  Client-side decoration (CSD) is the concept of allowing a software to be
  responsible for drawing its own window decorations. In this post you can
  learn how to trick GNOME Terminal to use client-side decoration even when
  non-GNOME desktop environment is used.
aliases: /howto/gnome-terminal-csd/
---

Enable CSD in GNOME Terminal
============================

Client-side decoration ([CSD]) is the concept of allowing a graphical
application software to be responsible for drawing its own window decorations,
historically the responsibility of the window manager. GNOME applications is
slowly migrating to client-side decoration. While some applications use CSD by
default, others draw them only while running in GNOME session.

![gnome-terminal with csd](headerbar.png)

Unfortunately, CSD is not used by GNOME Terminal if you launch it outside of
GNOME session. Fortunately, there's a configuration option you can use to
explicitly enable it. In order to do that just run the following command in
your terminal:

```bash
$ gsettings set org.gnome.Terminal.Legacy.Settings headerbar true
```

::: note
The setting won't be applied as long as there's a running copy of
`gnome-terminal-server` process. You have to terminate it and restart the
terminal.
:::

The configuration option is tested with `gnome-terminal 3.40`. It might or
might not work with other versions.

[CSD]: https://wiki.gnome.org/Initiatives/CSD
