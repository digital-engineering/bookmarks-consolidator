# Bookmarks Consolidator

### Joe Bashe 2019

This program takes two sets of bookmarks, exported as HTML from Firefox, 
Chrome, etc., and combines them together into an importable HTML file 
containing the combined bookmarks from both. Duplicate bookmarks are skipped,
and duplicate folders are merged.

## Usage

    python consolidate.py "bookmarks_file_1.html" "bookmarks_file_2.html"

A file `bookmarks_export.html` will be created as a result, containing 
consolidated bookmarks from both input files.