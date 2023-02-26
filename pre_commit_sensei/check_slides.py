#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Sequence


def check_chapters(filename) -> int:
    """Check that before each chapter lvl2 or lvl3, there is 3 empty lines.

    This is not compatible with Markdown standard, it's the reason why we disable rule MD012.
    """
    ret = 0
    with open(filename, "r", encoding="utf-8") as file:
        content = file.readlines()
        for i in range(0, len(content)):
            current_line = content[i]
            if current_line.startswith("## ") or current_line.startswith("### "):
                f = i - 3
                g = i - 2
                h = i - 1
                if (
                    len(content[f].rstrip())
                    or len(content[g].rstrip())
                    or len(content[h].rstrip())
                ):
                    ret = 1
                    print(80 * "-")
                    print(f"In file {filename} missing empty line to get new page")
                    print(str(f + 1) + ": " + content[f].rstrip())
                    print(str(g + 1) + ": " + content[g].rstrip())
                    print(str(h + 1) + ": " + content[h].rstrip())
                    print(str(i + 1) + ": " + current_line.rstrip())
                    print(80 * "-")
    return ret


def check_notes(filename) -> int:
    """Check that, if a line begin with `Notes` it means that lines after are notes for trainers.

    The right syntax is : `Notes :`. The line before must be empty.

    """
    ret = 0
    with open(filename, "r", encoding="utf-8") as file:
        content = file.readlines()
        for i in range(0, len(content)):
            current_line = content[i]

            if "Notes" in current_line:
                h = i - 1

                if "Notes" in current_line and current_line.rstrip() != "Notes :":
                    ret = 1
                    print(80 * "-")
                    print(f"In file {filename} you have to write `Notes :`")
                    print(str(i + 1) + ": " + current_line.rstrip())
                    print(80 * "-")

                if len(content[h].rstrip()):
                    ret = 1
                    print(80 * "-")
                    print(f"In file {filename} missing empty line to get notes")
                    print(str(h + 1) + ": " + content[h].rstrip())
                    print(str(i + 1) + ": " + current_line.rstrip())
                    print(80 * "-")
    return ret


def check_too_many_empty_lines(filename) -> int:
    """As we disable rule MD012, even so, we check there is no 4 consecutive empty lines."""

    ret = 0
    with open(filename, "r", encoding="utf-8") as file:
        content = file.readlines()
        for i in range(0, len(content)):
            f = i - 3
            g = i - 2
            h = i - 1
            if (
                len(content[f].rstrip()) == 0
                and len(content[g].rstrip()) == 0
                and len(content[h].rstrip()) == 0
                and len(content[i].rstrip()) == 0
            ):
                ret = 1
                print(80 * "-")
                print(f"In file {filename} too many empty line")
                print(str(i + 1) + ": " + content[i].rstrip())
                print(80 * "-")

    return ret


def main(argv: Sequence[str] | None = None) -> int:
    ret = 0
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    args = parser.parse_args(argv)

    for filename in args.filenames:
        if filename.startswith("Slides"):

            if check_chapters(filename) == 1:
                ret = 1

            if check_notes(filename) == 1:
                ret = 1

            if check_too_many_empty_lines(filename) == 1:
                ret = 1

    return ret


if __name__ == "__main__":
    raise SystemExit(main())
