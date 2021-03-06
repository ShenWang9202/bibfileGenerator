#!/usr/bib/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function, absolute_import
import argparse
import textwrap
from mytitle2bib.crossref import get_bib_from_title
import sys
import io
from unidecode import unidecode
pyversion = sys.version_info[0]


def save_output_bibs(bibs, output_file):
    with io.open(output_file, 'w', encoding = "utf-8") as bibfile:
        for bib in bibs:
            bibfile.write("{}\n".format(bib))


def main():
    parser = argparse.ArgumentParser(
        prog="title2bib",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Convert a list of titles in a bibfile.
        You also can convert a simple title, like:
        $ mytitle2bib  On boundary Dirac Equations
        or use the following command to get the first item and append
        in your bib file
        $ mytitle2bib  On boundary Dirac Equations --first >> refs.bib

        -----------------------------------------------------

            @author: Bruno Messias
            @email: messias.physics@gmail.com
            @telegram: @brunomessias
            @github: https://github.com/bibcure/title2bib
        ''')
    )

    parser.add_argument(
        "--input", "-i",
        help="input file"
    )
    parser.add_argument(
        "--output", "-o",
        help="bibtex output file")

    parser.add_argument("--first", "-f",
                        dest="first",
                        action="store_true",
                        help="get the first found"
                        )


    parser.set_defaults(first=False)

    args = parser.parse_known_args()
    get_first = args[0].first
    inlineTitle = len(args[1]) > 0
    if inlineTitle:
        titles = [" ".join([c if pyversion == 3 else c.decode(sys.stdout.encoding) for c in args[1]])]
    else:
        titles = args[0].input
        with io.open(titles, "r", encoding = "utf-8") as inputfile:
            titles = inputfile.read()
        titles = [t  for t in titles.split("\n") if t != ""]
    bibs = []

    for title in titles:
        found, bib = get_bib_from_title(title, get_first)
        if found:
            bibs.append(bib)

    if len(bibs) > 0:
        if inlineTitle:
            print("\n")
            print(bibs[0])
            print("\n")
        else:
            save_output_bibs(bibs, args[0].output)


if __name__ == "__main__":
    main()
