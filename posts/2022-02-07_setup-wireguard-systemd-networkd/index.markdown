---
summary: >-
  WireGuard is an extremely simple, fast and modern VPN that is built into
  Linux kernel. In this post you can learn more on how to setup a WireGuard VPN
  server on Linux using systemd-networkd network manager that is a part of most
  Linux distributions.
---

Setup a WireGuard server using systemd-networkd
===============================================

::: note
Please check out [«Setup a WireGuard client using systemd-networkd»][wg-client]
to learn about client-side configuration of your Linux machine.
:::

WireGuard is an extremely simple, fast and modern VPN that is built into Linux
kernel 5.6 (released on Mar 29, 2020) and above. It mimics the model of SSH and
requires VPN peers to know each others public keys. I highly recommend to read
<https://www.wireguard.com> regardless of this post.

When it comes to WireGuard, there's one interesting aspect: it has no notion of
'server', it's distributed by design and no blockchain is involved. Blockchain
enthusiasts may found this surprising but distributed software were invented
long before the blockchain 😅. Each peer may connect to other peers assuming
they know each other (i.e. public key, IP) and there's a connectivity between
them. The 'server' is rather a behaviour one may expect from a certain peer.
There are 3 key points that are normally expected from a 'server' peer:

 * The peer is publicly available, so other peers may connect to it even when
   behind SNAT.
 * The peer can act as a proxy and connect other peers into a single network.
 * The peer can act as a gateway to the Internet.

There are number of ways to configure WireGuard on a Linux machine. My favorite
one is to use [systemd-networkd], a system service that manages both networks
and network devices. It's distributed as part of systemd suite, so most likely
you have it installed, and it supports WireGuard starting with v237. It's a
good choice for a Linux server because it requires no extra software.

For instance we want to setup the following VPN network:

 | Option  | Value         |
 |:------- |:------------- |
 | Network | `10.0.0.0/24` |
 | Server  | `10.0.0.1`    |
 | Peer A  | `10.0.0.20`   |
 | Peer B  | `10.0.0.30`   |

First thing to do is to set up a virtual network device for a WireGuard tunnel.
This can be achieved by means of a [systemd.netdev(5)][systemd.netdev] unit
that must be created in `/etc/systemd/network/` directory. The WireGuard
network device must know about number of things:

 * The port to accept new connections on.
 * The private key of the server.
 * The list of known peers and their public keys.

This is how some `/etc/systemd/network/wg0.netdev` could look like:

```ini
[NetDev]
Name=wg0
Kind=wireguard
Description=wg0 - wireguard tunnel

[WireGuard]
ListenPort=51820
PrivateKeyFile=/etc/systemd/network/wg0.key

[WireGuardPeer]
AllowedIPs=10.0.0.20/32
PublicKey=9vzzasvYciJLmhjrt9Aj9aQYe1gnUxI44ShVLQPrDQA=

[WireGuardPeer]
AllowedIPs=10.0.0.30/32
PublicKey=9vzzasvYciJLmhjrt9Aj9aQYe1gnUxI44ShVLQPrDQA=
```

The content of `/etc/systemd/network/wg0.key` can be generated by invoking
`$ wg genkey` command and must be readable by the `systemd-network` user.
What's notable here is that `$ wg genkey` can be executed anywhere, even on
your laptop, there's no need to install extra software on the server.

Next thing to do is to use a [systemd.network(5)][systemd.network] unit to
setup a network. The purpose of the network is to assign a proper IP address on
the network device, set proper routes and so on.

This how some `/etc/systemd/network/wg0.network` could look like:

```ini
[Match]
Name=wg0

[Network]
Address=10.0.0.1/24
IPMasquerade=both
```

There are couple of things to note:

 * Since `/24` network mask is used, systemd-networkd will automatically add a
   route for the whole network to be routed via the WireGuard tunnel. Without
   that mask, it'd be up to a user to properly configure routing on the system.

 * The `IPMasquerade` setting is only needed if the server is expected to be
   used as a gateway to the Internet. Without this option, it'd be up to a user
   to properly configure the firewall.

When both the network device and the network are configured, the only remained
step is to run `$ networkctl reload` to pipe in and apply latest configuration.

[wg-client]: /posts/setup-wireguard-client-systemd-networkd/
[systemd-networkd]: https://man.archlinux.org/man/systemd-networkd.8.en
[systemd.netdev]: https://man.archlinux.org/man/systemd.netdev.5
[systemd.network]: https://man.archlinux.org/man/systemd.network.5
