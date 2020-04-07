#!/usr/bin/env python3
"""
consolidate.py - Bookmarks consolidator

 Takes two HTML bookmarks exports, from Firefox, Chrome, etc., and merges them
 into a single set of bookmarks. Outputs an bookmarks HTML file.

Usage:
    consolidate.py <bookmarks-A> <bookmarks-B>
    consolidate.py (-h|--help)

Arguments:
    <bookmarks-A> Bookmarks HTML file A
    <bookmarks-B> Bookmarks HTML file B
    (-h|--help)   This information screen

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
    bookmarks_a = bookmarks_parser.parse(arguments['<bookmarks-A>'])
    bookmarks_b = bookmarks_parser.parse(arguments['<bookmarks-B>'])

    bc = BookmarksConsolidator()
    res = bc.consolidate_bookmarks(bookmarks_a, bookmarks_b)
