Enable CSD in GNOME Terminal
============================

If you aren't using GNOME but for some reason want to use GNOME Terminal in
other desktop environments (e.g. Sway or XFCE), you just might want to embrace
client-side decoration ([CSD]), so it looks like this:

![gnome-terminal with csd](headerbar.png)

Unfortunately, CSD is not used by GNOME Terminal if you launch it outside of
GNOME. Fortunately, there's a configuration option you can use to explicitly
enable it. In order to do that just run the following command in your terminal:

```
$ gsettings set org.gnome.Terminal.Legacy.Settings headerbar true
```

Please note, the setting won't be applied as long as there's a running copy
of `gnome-terminal-server` process. You have to terminate it and restart the
terminal. The configuration option is tested with `gnome-terminal 3.40`. It
might or might not work with other versions.

[CSD]: https://wiki.gnome.org/Initiatives/CSD
