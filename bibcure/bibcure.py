from __future__ import unicode_literals, print_function, absolute_import
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import argparse
#import operator
import textwrap
#from itertools import groupby
#from multiprocessing import Pool
#from in_db import update_bibs_in
#from out_db import update_bibs_out
from arxiv import update_bibs_arxiv
from title import update_bibs_get_doi
#from doi import update_bibs_from_doi
from database import Db_abbrev
import io

db_abbrev = Db_abbrev()


def get_status(bib):
    text = ""
    state = "are_not_journal"

    if "journal" in bib:
        if "arxiv" in bib["journal"].lower():
            text = ""
            state = "are_arxiv"
        else:
            state = "are_out_db"
            expanded_index = db_abbrev.get_index(bib["journal"], key="name")
            abbrev_index = db_abbrev.get_index(bib["journal"], key="abbrev")
            if expanded_index != -1:
                text = db_abbrev.db[expanded_index]["abbrev"]
                state = "can_be_abbreviated"
            elif abbrev_index != -1:
                text = db_abbrev.db[abbrev_index]["name"]
                state = "can_be_expanded"
    bib["_type"] = state
    bib["_text"] = text

    return bib


def save_output_bib(updated_bibs, output_file):
    print('saving to ' + output_file)
    writer = BibTexWriter()
    new_bibtex = BibDatabase()
    new_bibtex.entries = updated_bibs
    # set to None to disable entries ordering
    writer.order_entries_by = None
    bibtex_string = writer.write(new_bibtex)
    try:
        with io.open(output_file, 'w', encoding="utf-8") as bibfile:
            bibfile.write(bibtex_string)

    except TypeError:
        print("Can't save in output file\n")
        print("Updated BibFile:\n")
        print(bibtex_string)


def main():
    parser = argparse.ArgumentParser(
        prog="bibcure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Bibcure helps in boring tasks by keeping
        your bibfile up to date and normalized.

        $ bibcure -i input.bib -o output.bib
        Given a bib file...

            . check sure the Arxiv items have been published, then update
                                    them(requires internet connection)
            . complete all fields(url, journal, etc) of all bib items using DOI
                                    number(requires internet connection)
            . find and create DOI number associated with each bib item which
                                    has not DOI field(requires internet
                                    connection)
            . abbreviate jorunals names

       $ doitobib 10.1038/s41524-017-0032-0
       Given a DOI number...

            . get bib item given a doi(requires internet connection)

       $ titletobib An useful paper
       Given a title...

            . search papers related and return a bib for the selected
                                    paper(requires internet connection)

       $ arxivcheck 1601.02785
       Given a arxiv id...

            . given an arixiv id, check if has been published, and then returns
                                    the updated bib (requires internet
                                    connection)
        -----------------------------------------------------
            @author: Bruno Messias
            @email: messias.physics@gmail.com
            @telegram: @brunomessias
            @github: https://github.com/bibcure/bibcure
        ''')
    )
    parser.add_argument(
        "--input", "-i",
        required=False,
        help="bibtex input file"
    )
    parser.add_argument(
        "--output", "-o",
        required=False,
        help="bibtex output file")

    args = parser.parse_args()
    #args.input = 'MyCollection.bib'
    #args.output = 'newbib.bib'
    dict_parser = {
        'keywords': 'keyword',
        'keyw': 'keyword',
        'subjects': 'subject',
        'urls': 'url',
        'link': 'url',
        'links': 'url',
        'editors': 'editor',
        'authors': 'author'}
    parser = bibtexparser.bparser.BibTexParser()
    parser.alt_dict = dict_parser
    inputfile = args.input
    with io.open(inputfile, "r", encoding="utf-8") as inputfile:
        bibtex = bibtexparser.loads(inputfile.read(), parser=parser)
    bibs = bibtex.entries
    #print(bibs)
    if len(bibs) == 0:
        print("Input File is empty or corrupted.")
        return
    #bibs = update_bibs_from_doi(bibs)
    bibs = update_bibs_get_doi(bibs)
    bibs = update_bibs_arxiv(bibs)
    #pool = Pool()
    #bibs = pool.map(get_status, bibs)
    #pool.close()
    #pool.join()

    #bibs.sort(key=operator.itemgetter('_type'))
    #bibs.reverse()
    save_output_bib(bibs, args.output)
    db_abbrev.close()


if __name__ == "__main__":
    main()
