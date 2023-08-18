ARG base_image=alpine:latest

FROM ${base_image} AS resource

RUN apk add --no-cache \
  bash \
  git \
  jq \
  python3 \
  py3-pip \
  openssh-client-default \
  openssh-client-common

COPY dist/nvmrc_version_resource-*-py3-none-any.whl /dist/
RUN pip install /dist/nvmrc_version_resource-*-py3-none-any.whl
