import time
from operator import itemgetter

from bookmarks_consolidator.html_exporter import HtmlExporter


class BookmarksConsolidator:
    # list of all bookmarks collected
    all_bookmarks = []
    # blacklisted bookmark titles
    blacklist_title = ['Most Visited', 'Unsorted', '', '', '', '', '', '', '', '', ]
    # blacklisted bookmark urls
    blacklist_url = ['https://www.mozilla.org/en-US/firefox/central/', ]

    def consolidate_bookmarks(self, firefox_bookmarks: list, chrome_bookmarks: list):
        # bookmarks toolbar
        firefox_bookmarks_bar = firefox_bookmarks[0]['children']
        chrome_bookmarks_bar = chrome_bookmarks[0]['children']

        # combine Bookmarks toolbar from firefox
        bookmarks_bar = self._combine_bookmarks(firefox_bookmarks_bar, chrome_bookmarks_bar)

        # bookmarks menu
        firefox_bookmarks_menu = firefox_bookmarks[2]['children']
        chrome_bookmarks_menu = chrome_bookmarks[1]['children']

        # combine Bookmarks menu
        bookmarks_menu = self._combine_bookmarks(firefox_bookmarks_menu, chrome_bookmarks_menu)

        # export firefox format
        he = HtmlExporter()
        he.export_html(bookmarks_bar, firefox_bookmarks[1], bookmarks_menu)

    def _combine_bookmarks(self, a: list, b: list) -> list:
        unique_in_a = self._diff_bookmark_list(a, b)
        unique_in_b = self._diff_bookmark_list(b, a)
        combined = unique_in_a + unique_in_b
        intersection = self._intersect_bookmark_list(a, b)
        for i in intersection:
            match: dict = next(j for j in b if i['type'] == j['type'] and (i['title'].lower() == j['title'].lower() or (
                    i['type'] == 'bookmark' and i['url'] == j['url'])))
            if i['type'] == 'bookmark':
                cb = self._consolidate_bookmark(i, match)
                combined.append(cb)
            else:
                children_in_i, children_in_match = 'children' in i, 'children' in match
                if not (children_in_i or children_in_match):
                    continue  # skip empty folder
                if children_in_i and children_in_match:
                    combined_children = self._combine_bookmarks(i['children'], match['children'])
                    del i['children'], match['children']
                    cb = self._consolidate_bookmark(i, match)
                    cb['children'] = combined_children
                    combined.append(cb)
                else:  # only in one
                    cb = self._consolidate_bookmark(i, match)
                    combined.append(cb)

        return list(sorted(combined, key=itemgetter('title')))

    @staticmethod
    def _consolidate_bookmark(a: dict, b: dict) -> dict:
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
    def _diff_bookmark_list(a, b):
        return [i for i in a if not next(
            (j for j in b if (i['type'] == j['type']) and (i['title'].lower() == j['title'].lower() or (
                    i['type'] == 'bookmark' and i['url'] == j['url']))), False)]

    @staticmethod
    def _intersect_bookmark_list(a, b):
        return [i for i in a if next(
            (j for j in b if (i['type'] == j['type']) and (i['title'].lower() == j['title'].lower() or (
                    i['type'] == 'bookmark' and i['url'] == j['url']))), False)]
