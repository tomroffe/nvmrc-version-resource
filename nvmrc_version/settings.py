from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    version_regex: str = Field(default=r"^v?(?P<major_version>\d+)\.?(?P<minor_version>\d+)?\.?(?P<patch_version>\d+)?", env="NVMRC_VERSION_REGEX")
    path: str = Field(default="", env="NVMRC_PATH")
    filename: str = Field(default=".nvmrc", env="NVMRC_FILENAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
