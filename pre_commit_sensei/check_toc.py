#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from typing import Sequence

TAG_RE = re.compile(r"<[^>]+>")


def remove_tags(text):
    return TAG_RE.sub("", text)


def check_on_chapter(filename, toc) -> int:
    ret = 0
    with open("Slides/" + filename, "r", encoding="utf-8") as chapter:
        content = chapter.readlines()

        # build toc from content, to check it below
        toc.append(
            {
                "filename": "Slides/" + filename,
                "title": content[0].rstrip(),
            }
        )

        # After title, HTML cosmetic is mandatory
        if content[2].rstrip() != '<!-- .slide: class="page-title" -->':
            ret = 1
            print(80 * "-")
            print(f"In filename {filename}, first slide must be page-title")
            print(80 * "-")

        # At the end of each chapter, HTML cosmetic is mandatory
        if (
            content[len(content) - 1].rstrip()
            != '<!-- .slide: class="page-questions" -->'
        ):
            ret = 1
            print(80 * "-")
            print(f"In file {filename}, last page must be page-questions")
            print(80 * "-")
    return ret


def check_toc_from_slides_json(filename) -> int:
    ret = 0
    toc = []

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        for file in data:
            check_on_chapter(file, toc)

    del toc[0]
    for idx, item in enumerate(toc):
        clean_text = remove_tags(item["title"][2:])
        item["toc"] = "- [" + clean_text + "](#/" + str(idx + 1) + ")"

    for item in toc:
        with open(item["filename"], "r", encoding="utf-8") as chapter:
            content = chapter.readlines()
            for i in range(0, len(content)):
                if content[i].rstrip() == '<!-- .slide: class="toc" -->':
                    begin = i + 2

                    for j in range(0, len(toc)):

                        current_line = content[begin + j].rstrip().replace("*", "")

                        if current_line != toc[j]["toc"]:
                            ret = 1
                            print(80 * "-")
                            print(
                                "In file "
                                + item["filename"]
                                + ", bad toc entry (expected : "
                                + toc[j]["toc"]
                                + ")"
                            )
                            print(str(begin + j + 1) + ": " + current_line)
                            print(80 * "-")
    return ret


def main(argv: Sequence[str] | None = None) -> int:
    """Check rules defined here :

    https://github.com/Zenika-Training/training-template/tree/main/Slides#r%C3%A8gles-de-r%C3%A9daction

    """
    ret = 0
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    args = parser.parse_args(argv)

    for filename in args.filenames:
        if filename == "Slides/slides.json":
            check_toc_from_slides_json(filename)

    return ret


if __name__ == "__main__":
    raise SystemExit(main())
