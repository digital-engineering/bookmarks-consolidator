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

bookmarks-consolidator is a CLI tool that combines and de-duplicates two sets of bookmarks. 
It accepts HTML files exported from Firefox, Chrome, etc., and consolidates them 
into an HTML file containing the combined bookmarks from both. 

Duplicate bookmarks are skipped, and duplicate folders are merged. Consolidate your bookmarks
from multiple browsers into one with this simple tool.

### Installation

```shell script
# Create virtual environment
python3 -m venv env

# Activate virtual environment (linux or git bash)
. env/bin/activate

# Install required packages
pip install -Ur requirements.txt
```

### Example usage

    python consolidate.py "bookmarks_1.html" "bookmarks_2.html"

A file `bookmarks_export.html` will be created as a result, containing 
consolidated bookmarks from both input files.
