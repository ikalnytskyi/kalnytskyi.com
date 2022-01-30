import re
import pathlib

import dateutil.parser
import dateutil.tz


def process(app, stream, /, *, pattern, timezone="UTC", trim=True):
    tzinfo = dateutil.tz.gettz(timezone)
    re_published = re.compile(pattern)

    for item in stream:
        if match := re_published.search(str(item["destination"])):
            published = dateutil.parser.parse(match.group("parse"), fuzzy=False)
            if not published.tzinfo:
                published = published.replace(tzinfo=tzinfo)
            item["published"] = published

            if trim:
                destination = (
                    match.string[: match.start("trim") + 1]
                    + match.string[match.end("trim") :]
                )
                item["destination"] = pathlib.Path(destination)
        yield item
