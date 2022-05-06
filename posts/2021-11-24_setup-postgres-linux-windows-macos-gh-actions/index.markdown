---
summary: >-
  GitHub Actions is a CI/CD platform integrated into your GitHub repository. In
  this post you can learn how to setup PostgreSQL server on any operating
  system supported by GitHub Actions, i.e. Windows, Linux and macOS.
aliases: /howto/setup-postgres-linux-windows-macos-gh-actions/
---

Setup PostgreSQL for Linux, Windows and macOS using GitHub Actions
==================================================================

GitHub Actions is a CI/CD platform that is widely used among open-source
software hosted on GitHub. If you happened to host your software there, you may
end up needing a SQL server to test your application. PostgreSQL is the most
common choice nowadays.

As of today (Nov 24, 2021), there's only one [action on the marketplace][0] to
setup a PostgreSQL server for Linux, Windows and macOS action runners. If you
among those who want to test their software on all major platforms, you have no
option but to use [ikalnytskyi/action-setup-postgres][1]. Below is the typical
usage example:

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

So why use that exact action and no other?

* Runs on Linux, macOS and Windows action runners.
* Fast! Preinstalled binaries are used.
* Easy to audit, just [4 steps YAML][2]!

[0]: https://github.com/marketplace/actions/setup-postgresql-for-linux-macos-windows
[1]: https://github.com/ikalnytskyi/action-setup-postgres
[2]: https://github.com/ikalnytskyi/action-setup-postgres/blob/v1/action.yml
