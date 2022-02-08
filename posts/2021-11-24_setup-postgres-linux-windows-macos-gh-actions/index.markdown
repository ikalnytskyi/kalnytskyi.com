---
summary: A note about how to setup PostgreSQL server on GitHub CI.
aliases: /howto/setup-postgres-linux-windows-macos-gh-actions/
---

Setup PostgreSQL for Linux, Windows and macOS using GitHub Actions
==================================================================

As of today (Nov 24, 2021), there's only [one action on the marketplace][0] to
setup a PostgreSQL server for Linux, Windows and macOS runners. If you among
those who want to test their software on all major platforms, you have no
option but to use [ikalnytskyi/action-setup-postgres][1].

```yaml
steps:
  - name: Setup PostgreSQL
    uses: ikalnytskyi/action-setup-postgres@v1
    id: postgres

  - name: Run tests
    env:
      CONNECTION_URI: ${{ steps.postgres.outputs.connection-uri }}
    run: pytest -vv tests/
```

Key features:

* Fast bootstrap (the action uses preinstalled binaries).
* Fast audit ([4 steps YAML][2], no javascript/typescript).

[0]: https://github.com/marketplace/actions/setup-postgresql-for-linux-macos-windows
[1]: https://github.com/ikalnytskyi/action-setup-postgres
[2]: https://github.com/ikalnytskyi/action-setup-postgres/blob/v1/action.yml
