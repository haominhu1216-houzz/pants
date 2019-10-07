#!/usr/bin/env python3
# Copyright 2019 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import re
from glob import glob
from typing import List

from common import die


def main() -> None:
    rust_files = find_files("src/rust/engine", extension=".rs")

    check_banned_import(
        rust_files,
        bad_import_regex=r"^use std::sync::.*(Mutex|RwLock)",
        correct_import_message="`parking_lot::(Mutex|RwLock)`",
    )


def find_files(*directories: str, extension: str) -> List[str]:
    return [
        fp
        for directory in directories
        for fp in glob(f"{directory}/**/*{extension}", recursive=True)
    ]


def filter_files(files: List[str], *, snippet_regex: str) -> List[str]:
    """Only return files that contain the snippet_regex."""
    regex = re.compile(snippet_regex)
    result: List[str] = []
    for fp in files:
        with open(fp, "r") as f:
            if any(re.search(regex, line) for line in f.readlines()):
                result.append(fp)
    return result


def check_banned_import(
    files: List[str], *, bad_import_regex: str, correct_import_message: str
) -> None:
    bad_files: List[str] = filter_files(files, snippet_regex=bad_import_regex)
    if bad_files:
        bad_files_str = "\n".join(bad_files)
        die(
            f"Found forbidden imports matching `{bad_import_regex}`. Instead, you should use "
            f"{correct_import_message}. Bad files:\n{bad_files_str}"
        )


if __name__ == "__main__":
    main()
