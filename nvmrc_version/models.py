from pydantic import BaseModel, computed_field, Json
from typing import Optional, Any


class Source(BaseModel):
    regex: Optional[str]
    path: Optional[str]
    filename: Optional[str]


class Version(BaseModel):
    ref: str


class InPayload(BaseModel):
    source: Source
    version: Version
    params: Optional[Json[Any]]


class NodeVersion(BaseModel):
    major_version: int
    minor_version: Optional[int]
    patch_version: Optional[int]
    nvmrc_version: str

    @property
    @computed_field
    def semver(self) -> str:
        semver: str
        semver = str(self.major_version)
        if self.minor_version:
            semver += ".{}".format(self.minor_version)
        if self.patch_version:
            semver += ".{}".format(self.patch_version)
        return semver
