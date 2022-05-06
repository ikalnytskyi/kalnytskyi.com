---
summary: >-
  Caddy 2 is an open source web server with automatic HTTPS which makes it a
  gread choice to be used as a reverse proxy. This post provides a recipe of
  how to configure sross-origin resource sharing (CORS) in Caddy.
aliases: /howto/setup-cors-caddy-2/
---

Setup CORS in Caddy 2
=====================

[Caddy 2] is an open source web server with automatic HTTPS. It's a wise choice
for pet projects or self-hosted services, since you are free from managing TLS
certs on your own and wiring things up can be super annoying.

One missing feature in Caddy 2, however, is cross-origin resource sharing
([CORS]) support. For a "batteries included" web server, it's rather
surprising. Fortunately, one can use the following [Caddy snippet] to augment
any site with CORS headers without repeating oneself over and over again.

::: note
You might want to update the list of headers returned by
`Access-Control-Allow-Headers` or `Access-Control-Expose-Headers` HTTP headers
according to your application needs. Please refer to the CORS documentation to
learn more what they are about.
:::

```
(cors) {
  @cors_preflight method OPTIONS
  @cors header Origin {args.0}

  handle @cors_preflight {
    header Access-Control-Allow-Origin "{args.0}"
    header Access-Control-Allow-Methods "GET, POST, PUT, PATCH, DELETE"
    header Access-Control-Allow-Headers "Content-Type"
    header Access-Control-Max-Age "3600"
    respond "" 204
  }

  handle @cors {
    header Access-Control-Allow-Origin "{args.0}"
    header Access-Control-Expose-Headers "Link"
  }
}

example.com {
  import cors https://example.com
  reverse_proxy localhost:8080
}
```

The nice part about this snippet is that CORS headers are only returned for
HTTP requests with the `Origin` HTTP header. That header is normally used by
browsers only, which means you won't see CORS headers in responses for requests
sent by `curl` or *your-programming-language-of-choice*.

I've been successfully using this snippet for quite a while now [to protect]
[api.xsnippet.org], so it can be accessed by [xsnippet.org].

[Caddy 2]: https://caddyserver.com/
[CORS]: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
[Caddy snippet]: https://caddyserver.com/docs/caddyfile/concepts#snippets
[to protect]: https://github.com/xsnippet/xsnippet-infra/blob/1d583a6868597cb71bb2ae08f60bc42ac4364e91/roles/xsnippet_api/templates/caddy.j2#L1-L17
[api.xsnippet.org]: https://api.xsnippet.org
[xsnippet.org]: https://xsnippet.org
