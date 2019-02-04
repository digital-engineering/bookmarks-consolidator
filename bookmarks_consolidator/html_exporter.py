import time


class HtmlExporter:
    def export_html(self, bookmarks_bar, other_bookmarks, bookmarks_menu):
        """Export NETSCAPE-Bookmark-file-1 format HTML bookmarks file."""
        filepath = 'bookmarks_export.html'
        output_file = open(filepath, mode='w', encoding='utf-8')
        timestamp = str(int(time.time()))
        # Header
        output_file.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks Menu</H1>
    <DL><p>""".format(timestamp, timestamp))
        self._create_html_node(output_file, bookmarks_menu, timestamp, 0)

        output_file.write("""
        <DT><H3 ADD_DATE="{}" LAST_MODIFIED="{}" UNFILED_BOOKMARKS_FOLDER="true">Other Bookmarks</H3>
    """.format(timestamp, other_bookmarks['add_date']))
        self._create_html_node(output_file, other_bookmarks['children'], timestamp, 1)

        output_file.write("""
        <DT><H3 ADD_DATE="{}" LAST_MODIFIED="{}" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks Toolbar</H3>
        <DD>Add bookmarks to this folder to see them displayed on the Bookmarks Toolbar
    """.format(timestamp, other_bookmarks['add_date']))
        self._create_html_node(output_file, bookmarks_bar, timestamp, 1)

        output_file.write("\n</DL>\n")
        output_file.close()

    def _create_html_node(self, output_file, bookmarks, timestamp, level):
        base_space = '    ' * level
        if level > 0:
            output_file.write("\n{}<DL><p>".format(base_space))

        for item in bookmarks:
            if item['type'] == 'bookmark':
                output_file.write("""\n{}<DT><A HREF="{}" ADD_DATE="{}" LAST_MODIFIED="{}">{}</A>""".format(
                    base_space + (4 * ' '), item['url'], item['add_date'], timestamp, item['title']))
            else:
                output_file.write("""\n{}<DT><H3 ADD_DATE="{}" LAST_MODIFIED="{}">{}</H3>""".format(
                    base_space + (4 * ' '), item['add_date'], timestamp, item['title'], base_space + (8 * ' ')))

                self._create_html_node(output_file, item['children'], timestamp, level + 1)

        if level > 0:
            output_file.write("\n{}</DL><p>".format(base_space))
