#!/usr/bin/env python3
"""
consolidate.py - Bookmarks consolidator

Takes two sets of bookmarks, exported as HTML from Firefox, Chrome, etc., and
combines them together into an importable HTML file.

Usage:
    consolidate.py <firefox-bookmarks> <chrome-bookmarks>
    consolidate.py (-h|--help)

Arguments:
    <firefox-bookmarks> Name of MLS
    <chrome-bookmarks>  Name of RETS Resource
    (-h|--help)         This information screen

"""

import bookmarks_parser
import docopt

from bookmarks_consolidator.bookmarks_consolidator import BookmarksConsolidator

if __name__ == "__main__":
    arguments = []
    try:
        # Parse arguments, use file docstring as a parameter definition
        arguments = docopt.docopt(str(__doc__))
    except docopt.DocoptExit as de:
        print(de)
        exit(1)

    # parse and load HTML bookmarks files
    bookmarks_a = bookmarks_parser.parse(arguments['<firefox-bookmarks>'])
    bookmarks_b = bookmarks_parser.parse(arguments['<chrome-bookmarks>'])

    bc = BookmarksConsolidator()
    res = bc.consolidate_bookmarks(bookmarks_a, bookmarks_b)
