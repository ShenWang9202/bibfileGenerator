from __future__ import unicode_literals, print_function, absolute_import
from builtins import input
from mytitle2bib.crossref import get_bib_from_title
import bibtexparser


def update_bib(bib, get_first=True):
    bib_id = bib["ID"]
    if "title" in bib:
    #if "doi" not in bib and "title" in bib:
        title_data = bib["title"]
        #print(title_data+" sldfj")
        title_data = title_data.replace("{", "")
        title_data = title_data.replace("}", "")

        title_data = title_data.replace("'", "")
        title_data = title_data.replace("'", "")
        #print(title_data+" sxxx")
        found, bib_string = get_bib_from_title(title_data, get_first)
        if found:
            bibentries = bibtexparser.loads(bib_string).entries
            if len(bibentries) != 0:
                bib = bibentries[0]
                print(bib["title"] + " updated!")
            else:
                print(bib["title"]+" found, but cannot be parsed by bibtexparser")
                return False
    bib["ID"] = bib_id
    return bib


def update_bibs_get_doi(bibs):
    action = input("Get DOI absent using the title?y(yes, automatic)/m(manual)/n(do nothing)")

    if action not in ("y", "m", "n"):
        return update_bibs_get_doi(bibs)
    lenofbib = len(bibs)
    if action != "n":
        get_first = True if action == "y" else False
        for i, bib in enumerate(bibs):
            print("\n" + str(i) + " of " + str(lenofbib) + "\n")
            bibupdated = update_bib(bib, get_first)
            if bibupdated:
                bibs[i] = bibupdated
    return bibs