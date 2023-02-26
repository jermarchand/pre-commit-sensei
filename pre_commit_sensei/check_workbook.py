#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
from typing import Sequence


def check_workbook_json() -> int:
    """Check that all Markdown files in Workbook folder are also present in `workbook.json`.

    If a file is not in the json list, it failed.
    """
    ret = 0

    with open("Workbook/workbook.json", "r", encoding="utf-8") as workbook:
        content = workbook.read()
        files = glob.glob("Workbook/*.md")
        for path in files:
            if path[9:] not in content:
                print(80 * "-")
                print(f"File `{path}` not found in `Workbook/workbook.json`")
                print(80 * "-")

    return ret


def check_strigo_json() -> int:
    """Check that all Markdown files in Workbook folder are also present in `.strigo/config.yml`.

    If a file is not in the json list, it failed.
    """
    ret = 0
    with open(".strigo/config.yml", "r", encoding="utf-8") as workbook:
        content = workbook.read()
        files = glob.glob("Workbook/*.md")
        for path in files:
            if path[9:] not in content:
                print(80 * "-")
                print(f"File `{path}` not found in `.strigo/config.yml`")
                print(80 * "-")

    return ret


def main(argv: Sequence[str] | None = None) -> int:
    """Check that all Markdown files in Workbook are used for Slides in PDF and Strigo"""
    ret = 0
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    args = parser.parse_args(argv)

    for filename in args.filenames:
        if filename.startswith("Workbook/workbook.json"):
            if check_workbook_json() == 1:
                ret = 1

        if filename.startswith(".strigo/config.yml"):
            if check_strigo_json() == 1:
                ret = 1

    return ret


if __name__ == "__main__":
    raise SystemExit(main())
