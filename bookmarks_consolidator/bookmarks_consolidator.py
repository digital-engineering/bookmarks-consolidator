import functools

from bookmarks_consolidator.html_exporter import HtmlExporter


class BookmarksConsolidator:
    """Recursively consolidate, merge, and combine two trees of bookmarks."""

    # list of all bookmarks collected
    all_bookmarks = []
    # blacklisted bookmark titles
    blacklist_title = ['Most Visited', 'Unsorted', ]
    # blacklisted bookmark urls
    blacklist_url = ['https://www.mozilla.org/en-US/firefox/central/', ]

    def consolidate_bookmarks(self, bookmarks_a: list, bookmarks_b: list):
        """Consolidate two trees of bookmarks."""
        bookmarks_bar_a, other_bookmarks_a, bookmarks_menu_a = self._separate_bookmarks_sections(bookmarks_a)
        bookmarks_bar_b, other_bookmarks_b, bookmarks_menu_b = self._separate_bookmarks_sections(bookmarks_b)

        # combine Bookmarks toolbar
        bookmarks_bar = self._combine_bookmarks(bookmarks_bar_a, bookmarks_bar_b)
        # combine Bookmarks menu
        bookmarks_menu = self._combine_bookmarks(bookmarks_menu_a, bookmarks_menu_b)
        # get "Other Bookmarks"
        other_bookmarks = self._consolidate_other_bookmarks(other_bookmarks_a, other_bookmarks_b)

        # export firefox format
        he = HtmlExporter()
        he.export_html(bookmarks_bar, bookmarks_menu, other_bookmarks)

    def _consolidate_other_bookmarks(self, other_bookmarks_a, other_bookmarks_b):
        """Consolidate two sets of "Other Bookmarks" and return result."""
        if other_bookmarks_a and other_bookmarks_b is None:
            other_bookmarks = other_bookmarks_a
        elif other_bookmarks_a is None and other_bookmarks_b:
            other_bookmarks = other_bookmarks_b
        elif other_bookmarks_a and other_bookmarks_b:
            other_bookmarks = self._combine_bookmarks(other_bookmarks_a, other_bookmarks_b)
        else:
            other_bookmarks = []
        return other_bookmarks

    def _combine_bookmarks(self, a: list, b: list) -> list:
        """Given two lists of bookmarks and folders, get those unique in A, those unique in B, and finally find
        intersection of those in both. Recursively descend through any folders."""
        unique_in_a = self._diff_bookmark_list(a, b)
        unique_in_b = self._diff_bookmark_list(b, a)
        combined = unique_in_a + unique_in_b
        intersection = self._intersect_bookmark_list(a, b)
        for i in intersection:
            m: dict = next(j for j in b if i['type'] == j['type'] and (i['title'].lower() == j['title'].lower() or (
                    i['type'] == 'bookmark' and i['url'] == j['url'])))
            if i['type'] == 'bookmark':
                cb = self._consolidate_bookmark(i, m)
                combined.append(cb)
            else:
                children_in_i, children_in_match = 'children' in i, 'children' in m
                if not (children_in_i or children_in_match):  # skip empty folder
                    continue
                if children_in_i and children_in_match:  # both have bookmarks, combine trees
                    combined_children = self._combine_bookmarks(i['children'], m['children'])
                    del i['children'], m['children']
                    cb = self._consolidate_bookmark(i, m)
                    cb['children'] = combined_children
                    combined.append(cb)
                else:  # only in one
                    cb = self._consolidate_bookmark(i, m)
                    combined.append(cb)

        combined.sort(key=functools.cmp_to_key(self._sort_bookmarks))

        return combined

    @staticmethod
    def _consolidate_bookmark(a: dict, b: dict) -> dict:
        """Given two bookmarks, a and b, get set of all keys from each and build a new bookmark combining as much data
        as possible from both."""
        r = {}
        keys = list(set(list(a.keys()) + list(b.keys())))
        for k in keys:
            a_val = a.get(k, None)
            b_val = b.get(k, None)
            if a_val == b_val:
                r[k] = a_val
            elif a_val and (b_val is None or b_val == ''):
                r[k] = a_val
            elif b_val and (a_val is None or a_val == ''):
                r[k] = b_val
            elif b_val and a_val:
                if k == 'add_date':  # keep oldest add date
                    r[k] = b_val if b_val < a_val else a_val
                elif k == 'last_modified':  # keep newest last_modified
                    r[k] = b_val if b_val > a_val else a_val
                else:  # otherwise keep longest string
                    r[k] = b_val if len(b_val) > len(a_val) else a_val
            else:
                raise Exception('Unexpected condition')

        return r

    @staticmethod
    def _diff_bookmark_list(a: list, b: list) -> list:
        """Given two lists of bookmarks and folders, find elements in A not in B."""
        return [i for i in a if not next(
            (j for j in b if (i['type'] == j['type']) and (i['title'].lower() == j['title'].lower() or (
                    i['type'] == 'bookmark' and i['url'] == j['url']))), False)]

    @staticmethod
    def _intersect_bookmark_list(a, b):
        """Given two lists of bookmarks and folders, find elements in A and B."""
        return [i for i in a if next(
            (j for j in b if (i['type'] == j['type']) and (i['title'].lower() == j['title'].lower() or (
                    i['type'] == 'bookmark' and i['url'] == j['url']))), False)]

    @staticmethod
    def _separate_bookmarks_sections(bookmarks):
        """Determine whether Chrome or Firefox bookmarks, and return bookmarks_bar, other_bookmarks, and
        bookmarks_menu sections.
        """
        if len(bookmarks) == 2:  # Chrome
            return bookmarks[0]['children'], None, bookmarks[1]['children']
        else:  # 3 == Firefox
            return bookmarks[0]['children'], bookmarks[1], bookmarks[2]['children']

    @staticmethod
    def _sort_bookmarks(a: dict, b: dict):
        """Comparator to sort bookmark dicts by reverse alphabetical for 'type', then alphabetical for 'title'."""
        title_a, title_b = a['title'].lower(), b['title'].lower()
        if a['type'] == b['type']:  # if their type is the same (folder or bookmark)
            return 1 if title_b < title_a else (-1 if title_a < title_b else 0)
        else:  # their type is not matched
            if b['type'] == 'folder':  # give `b` first priority if it is folder
                return 1
            else:  # otherwise give `a` priority
                return -1
