import pathlib

import holocron


def process(app, stream, *, template="redirect.j2"):
    for item in stream:
        yield item

        if aliases := item.get("aliases"):
            if isinstance(aliases, str):
                aliases = [aliases]

            for alias in aliases:
                if not alias.endswith((".html", ".htm")):
                    alias = f"{alias}/index.html"
                alias = alias.lstrip("/")
                yield holocron.WebSiteItem(
                    {
                        "source": pathlib.Path(f"alias://{item['source']}"),
                        "destination": pathlib.Path(alias),
                        "template": template,
                        "baseurl": app.metadata["url"],
                        "original": item,
                    }
                )
