from datetime import date, datetime

from pydantic import BaseModel, computed_field, Json
from typing import Optional, Any, List


class Source(BaseModel):
    regex: Optional[str] = None
    path: Optional[str] = None
    filename: Optional[str] = None


class Version(BaseModel):
    ref: str


class InPayload(BaseModel):
    source: Optional[Source] = None
    version: Version


class CheckPayload(BaseModel):
    source: Optional[Source] = None
    version: Version
    params: Optional[Json[Any]] = None


class NodeVersion(BaseModel):
    major_version: int
    minor_version: Optional[int] = None
    patch_version: Optional[int] = None
    nvmrc_version: str

    @computed_field  # type: ignore[misc]
    @property
    def semver(self) -> str:
        semver: str
        semver = str(self.major_version)
        if self.minor_version:
            semver += ".{}".format(self.minor_version)
        if self.patch_version:
            semver += ".{}".format(self.patch_version)
        return semver


class InOutputMetadataItem(BaseModel):
    name: str
    value: str


class InOutput(BaseModel):
    version: Version
    metadata: Optional[List[InOutputMetadataItem]]


class NPMVersion(BaseModel):
    version: str
    date: date
    files: List[str]
    npm: Optional[str] = None
    v8: Optional[str] = None
    uv: Optional[str] = None
    zlib: Optional[str] = None
    openssl: Optional[str] = None
    modules: Optional[str] = None
    lts: bool | str
    security: bool


class RegistryTagImage(BaseModel):
    architecture: str
    features: str
    variant: Optional[str] = None
    digest: Optional[str] = None
    os: str
    os_features: str
    os_version: Optional[str] = None
    size: int
    status: str
    last_pulled: Optional[datetime] = None
    last_pushed: Optional[datetime] = None


class RegistryTag(BaseModel):
    creator: int
    id: int
    last_updated: Optional[datetime] = None
    last_updater: int
    last_updater_username: str
    name: str
    repository: int
    full_size: int
    v2: bool
    tag_status: str
    tag_last_pulled: Optional[datetime] = None
    tag_last_pushed: Optional[datetime] = None
    media_type: Optional[str] = None
    content_type: Optional[str] = None
    digest: Optional[str] = None
    images: List[RegistryTagImage]

    def __eq__(self, other: object) -> bool:
        if self.id == other.id:
            return True
        else:
            return False


class RegistryResults(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[RegistryTag]


class RegistryTagDigest(BaseModel):
    name: str
    digest: Optional[str] = None
    architectures: Optional[List[str]]
    aliases: Optional[List[str]]
