from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    version_regex: str = Field(default=r"^v?(?P<major_version>\d+)\.?(?P<minor_version>\d+)?\.?(?P<patch_version>\d+)?", validation_alias="NVMRC_VERSION_REGEX")
    path: str = Field(default="", validation_alias="NVMRC_PATH")
    filename: str = Field(default=".nvmrc", validation_alias="NVMRC_FILENAME")

    versions_url: str = Field(default="https://nodejs.org/download/release/index.json", validation_alias="NVMRC_VERSIONS_URL")
    registry_url: str = Field(default="https://registry.hub.docker.com/v2/repositories/library/node/tags?page_size=1000", validation_alias="NVMRC_REGISTRY_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
