import typing as t
import subprocess


def process(app, stream, *, commands: t.List[str]):
    yield from stream

    for command in commands:
        subprocess.check_call(command, shell=True)
