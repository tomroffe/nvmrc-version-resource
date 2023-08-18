import json
import re
import sys
import os

from rich import print_json

from pydantic import ValidationError

from nvmrc_version.logs import log
from nvmrc_version.settings import Settings
from nvmrc_version.models import InPayload, NodeVersion


def main():
    destination_path = check_destination_path(sys.argv[1])
    request_payload = load_request_payload()
    in_(destination_path, request_payload)


def check_destination_path(path: str) -> str:
    if os.path.exists(path):
        log.info("[gray]Destination Path[/gray]: [green]{}[/green]".format(path))
    else:
        log.error("[red]Invaild Path[/red]")
        exit(1)
    return path


def load_request_payload() -> InPayload:
    try:
        request_payload = InPayload(**json.load(sys.stdin))
        return request_payload
    except ValidationError as e:
        log.exception(f"[bold red]Validation Error[/bold red]: {e.errors()}")
        exit(1)


def get_nvmrc_version(destination_path: str, payload: InPayload) -> str:
    file = "{}/{}".format(destination_path, Settings().filename)
    with open(file, "r", encoding="utf8") as fh:
        raw_version = fh.readline()
        info = "[gray]Found [green]{}[/green]\n  Version [/gray]: [green]{}[/green]".format(Settings().filename, raw_version)
        log.info(info)
    return raw_version


def get_nvmrc_regex(payload: InPayload) -> re.Pattern[str]:
    try:
        source = payload.source.regex
        if source:
            regex = re.compile(source)
    except AttributeError:
        regex = re.compile(Settings().version_regex)
    return regex


def in_(destination_path: str, payload: InPayload):
    version = get_nvmrc_version(destination_path, payload)
    regex = get_nvmrc_regex(payload)

    match = regex.match(version)
    if match is not None:
        nvmrc_version = match.string
        output = match.groupdict()
    else:
        log.error("[red]Invaild Path[/red]")
        exit(1)

    semver = NodeVersion(**output, nvmrc_version=nvmrc_version)
    print_json(semver.model_dump_json())
    # print("[italic red]Hello[/italic red] World!", locals())


if __name__ == "__main__":
    main()
