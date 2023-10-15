import typer

from typing import List
from datetime import timedelta
from requests_cache import CachedSession

from rich import print, print_json

from nvmrc_version.logs import log
from nvmrc_version.settings import Settings
from nvmrc_version.models import NPMVersion, RegistryResults, RegistryTag, RegistryTagDigest


app = typer.Typer()


class VersionSpider:
    def __init__(self) -> None:
        self.url = Settings().versions_url
        self.session = CachedSession("nvmrc_version_cache", expire_after=timedelta(hours=24))

    def get_versions(self) -> List[NPMVersion]:
        response = self.session.get(self.url)
        return [NPMVersion(**version) for version in response.json()]


class RegistryTagsSpider:
    def __init__(self) -> None:
        self.tags: List[RegistryTag] = []
        self.digests: List[RegistryTagDigest] = []
        self.url: str = Settings().registry_url
        self.session: CachedSession = CachedSession("nvmrc_version_cache", expire_after=timedelta(hours=24), cache_control=False)

    def _get_tags_request(self, url: str):
        response = self.session.get(url)
        result = RegistryResults(**response.json())
        log.info(f"[white]Fetching Tags: [blue]{len(self.tags)}[/blue]/[magenta]{result.count - len(self.tags)}[/magenta]/[cyan]{result.count}[/cyan][/white]")
        for tag in result.results:
            self.tags.append(tag)
        if result.next:
            log.info("Fetched Next Page...")
            self._get_tags_request(result.next)

    def _get_digests(self) -> List[RegistryTagDigest]:
        log.info("Generating Digests...")
        for item in self.tags:
            log.info(f"Generating Digest for {item.name}")
            self.digests.append(self._get_digest(item))
        return self.digests

    def _get_digest(self, request: RegistryTag) -> RegistryTagDigest:
        log.info(f"Generating Digest for {request.name}")
        archs = [image.architecture for image in request.images]
        aliases = [tag for tag in self.tags if tag.digest == request.digest and tag.name != request.name]
        aliases_names = [alias.name for alias in aliases]
        return RegistryTagDigest(name=request.name, digest=request.digest, architectures=archs, aliases=aliases_names)

    def find_tag(self, tag: str):
        

    def get_digests(self) -> List[RegistryTagDigest]:
        if self.digests:
            return self.digests
        else:
            if self.tags:
                return self._get_digests()
            else:
                self._get_tags_request(self.url)
                return self._get_digests()

    def get_tags(self) -> List[RegistryTag]:
        if self.tags:
            return self.tags
        else:
            self._get_tags_request(self.url)
            return self.tags


@app.command()
def versions():
    v = VersionSpider()
    for version in v.get_versions():
        print(version)


@app.command()
def tags():
    t = RegistryTagsSpider()
    data = t.get_tags()


@app.command()
def digests():
    t = RegistryTagsSpider()
    print(t.get_digests())


@app.command()
def digest(tag: str):
    t = RegistryTagsSpider()
    data = t.get_digests()
    for item in data:
        if item.name == tag:
            print(item)


def main():
    app()


if __name__ == "__main__":
    app()
