Bookmarks Consolidator
======================

### Summary

>#### consolidate
>
>*verb (used with object)*, **con·sol·i·dat·ed**, **con·sol·i·dat·ing**.
>
>1. to bring together (separate parts) into a single or unified whole; unite; 
>combine: They consolidated their three companies.
>2. to discard the unused or unwanted items of and organize the remaining: She
>consolidated her home library.
>3. to make solid or firm; solidify; strengthen: to consolidate gains. 

bookmarks-consolidator combines and de-duplicates two sets of bookmarks. 
Accepts HTML files exported from Firefox, Chrome, etc., and consolidates them 
into an importable HTML file containing the combined bookmarks from both. 
Duplicate bookmarks are skipped, and duplicate folders are merged.

### Example

    python consolidate.py "bookmarks_1.html" "bookmarks_2.html"

A file `bookmarks_export.html` will be created as a result, containing 
consolidated bookmarks from both input files.