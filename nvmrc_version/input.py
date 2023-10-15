import json
import re
import sys
import os

from rich import print_json

from pydantic import ValidationError
from typing import Optional, cast

from nvmrc_version.logs import log
from nvmrc_version.settings import Settings
from nvmrc_version.models import InPayload, NodeVersion, Source, InOutput, InOutputMetadataItem, Version


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
        info = f"[gray]Found [green]{Settings().filename}[/green]\nRaw Version Value[/gray]: [green]{raw_version}[/green]"
        log.info(info)
    return raw_version


def get_nvmrc_regex(payload: InPayload) -> re.Pattern[str]:
    regex: re.Pattern[str]

    if isinstance(payload.source, Source):
        source = payload.source
        if source.regex:
            regex = re.compile(source.regex)
        else:
            regex = re.compile(Settings().version_regex)
    else:
        regex = re.compile(Settings().version_regex)
    return regex


def in_(destination_path: str, payload: InPayload):
    source_version = get_nvmrc_version(destination_path, payload)
    regex = get_nvmrc_regex(payload)

    match = regex.match(source_version)
    if match is not None:
        nvmrc_version = match.string
        result = match.groupdict()
    else:
        log.error("[red]Invaild Path[/red]")
        exit(1)

    mjv: int = cast(int, result.get("major_version"))
    miv: Optional[int] = cast(int, result.get("minor_version"))
    pv: Optional[int] = cast(int, result.get("patch_version"))
    semver = NodeVersion(major_version=mjv, minor_version=miv, patch_version=pv, nvmrc_version=nvmrc_version)
    log.info(f"SemVer: {semver}")

    version = Version(ref=semver.semver)
    log.info(f"Reference Version: {version}")

    metadata = [InOutputMetadataItem(name=item[0], value=str(item[1])) for item in semver.model_dump().items()]
    log.info(f"Compiled Metadata: {metadata}")

    output = InOutput(version=version, metadata=metadata)
    print_json(output.model_dump_json())


if __name__ == "__main__":
    main()
