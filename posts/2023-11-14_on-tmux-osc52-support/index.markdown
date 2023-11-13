---
summary: >-
  OSC-52, NeoVim and surprising behavior when running under tmux.
---

On tmux OSC-52 support
======================

Several days ago, OSC-52 support was [merged][1] into NeoVim, and this sparkled
my interest. It was just natural, given that both NeoVim and OSC-52 are
essential part of my daily workflow.

For those unfamiliar, OSC stands for _Operating System Command_, and it's a set
of [escape sequences][2] originally [defined by Xterm][3], but now adopted by
various modern terminal emulators[^1]. OSC-52, in particular, is an escape
sequence that allows _copying to_ and _pasting from_ the system clipboard.

I have a few development environments running in virtual machines or
systemd-nspawn containers, and I typically SSH into them and run NeoVim from
within. Needless to say that a NeoVim instance running inside container has no
access to the system clipboard[^2], and this is where OSC-52 comes to the
rescue!

```dot { "exec": ["dot", "-Tsvg"] }
digraph G {
    pencolor = "#2E3440"
    style = dashed

    node [shape = box, color = "#2E3440"]
    edge [arrowhead = open]

    subgraph cluster_Host {
        label = "Host"

        subgraph cluster_VM {
            label = "VM"

            neovim1 [label="NeoVim"]
        }

        subgraph cluster_Container1 {
            label = "Container"

            neovim2 [label="NeoVim"]
        }

        subgraph cluster_Container2 {
            label = "Container"

            neovim3 [label="NeoVim"]
        }
    }
}
```

If your terminal emulator supports it, NeoVim's built-in OSC-52 clipboard
provider just works! Here's the thing though: if you're a blessed user of tmux,
things might not go the way you expect them to go. I quickly noticed a peculiar
behavior that I initially mistook for a bug: OSC-52 pasting didn't paste the
content of the system clipboard, but rather the content of tmux top buffer.

Despite being called a multiplexer, tmux acts as a terminal emulator, which
means it implements many OSC sequences itself, including OSC-52. When it comes
to copying, tmux saves captured text to its buffer and passes the escape
sequence up to the parent terminal to set the system clipboard. Pasting, on the
other hand, always retrieves a content from a tmux buffer, forms a response and
passes it up to the parent terminal for pasting. The content of the buffer may
be a text you previously copied (and hence implicitly saved) or a text you
explicitly saved to a buffer.

What does this mean practically? It means that a text you copy in NeoVim can be
pasted in a browser. However, a text that you copied in a browser cannot be
pasted to NeoVim. Lame, huh?

Unfortunately, this is intentional behavior because tmux supports multiple
clients that may be attached from multiple hosts[^3]. It's a no-brainer with
copying: we just send a text we want to copy to all clients and let their
terminal emulators to set the system clipboard. But what should we do with
pasting? What attached client should be used as a clipboard source?

```dot { "exec": ["dot", "-Tsvg"] }
digraph G {
    pencolor = "#2E3440"
    style = dashed

    node [shape = box, color = "#2E3440"]
    edge [arrowhead = open]

    subgraph cluster_Host1 {
        label = "Host A"

        tmux_server [label="tmux server"]
        tmux_client1 [label="tmux client"]
    }

    subgraph cluster_Host2 {
        label = "Host B"

        tmux_client2 [label="tmux client"]
    }


    tmux_server -> tmux_client1 [dir=back]
    tmux_server -> tmux_client2 [dir=back]
}
```

Fortunately, tmux gives us a command, `refresh-client -l`, that can be executed
by any client to sync the content of the system clipboard to a tmux buffer,
that can subsequently be used to paste the content via OSC-52.

I decided to share this information, as I spent at least an hour running tmux
under gdb, chasing a ghost that doesn't exist. I don't want anyone to repeat my
experience.


[^1]: OSC-52 is at least supported by alacritty, contour, foot, hterm, iterm2,
      kitty, rxvt, st, tmux, wezterm, windows terminal and zelij.

[^2]: In my case, VMs and containers have no access to the wayland socket, and
      I don't want them to.

[^3]: <https://github.com/tmux/tmux/issues/1477#issuecomment-421344891>

[1]: https://github.com/neovim/neovim/pull/25872
[2]: https://en.wikipedia.org/wiki/ANSI_escape_code
[3]: https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-Operating-System-Commands
