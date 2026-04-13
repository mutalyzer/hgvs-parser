from __future__ import annotations

from importlib.metadata import metadata

from .convert import to_model
from .hgvs_parser import parse

__all__ = ["parse", "to_model"]


def _get_metadata(name: str) -> str:
    meta = metadata(__package__)
    return meta.get(name) or ""


def _get_homepage() -> str:
    meta = metadata(__package__)
    for project_url in meta.get_all("Project-URL") or []:
        label, url = project_url.split(", ", 1)
        if label == "Homepage":
            return url
    return ""


_copyright_notice = "Copyright (c) {}".format(_get_metadata("Author-email"))

usage = [_get_metadata("Summary"), _copyright_notice]


def doc_split(func: object) -> str:
    return (func.__doc__ or "").split("\n\n")[0]


def version(name: str) -> str:
    return "{} version {}\n\n{}\nHomepage: {}".format(
        _get_metadata("Name"),
        _get_metadata("Version"),
        _copyright_notice,
        _get_homepage(),
    )
