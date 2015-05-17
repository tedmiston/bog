"""
Generate the notes outline for a book.
"""

import argparse

import yaml

from models import Author, Chapter, Notes, Outline, Section, TableOfContents, TitleBlock


UNNUMBERED_MARK = '.'  # prefix to hide numbering on chapters like Preface
DEFAULT_OUTPUT_FILENAME = 'output.md'


def setup():
    """Parse command-line args."""
    parser = argparse.ArgumentParser(description='Generate the notes outline for a book.')
    parser.add_argument('input', type=argparse.FileType('r'),
                        help='metadata and table of contents file in yaml format')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), required=False,
                        default=DEFAULT_OUTPUT_FILENAME,
                        help='output file name (default: %s)' % (DEFAULT_OUTPUT_FILENAME))
    args = parser.parse_args()
    return args


class YAMLParser(object):
    """Parse a YAML input file into native objects."""

    def __init__(self, input_file):
        self.input_file = self._load_input_file(input_file)

    def _load_input_file(self, input_file):
        return yaml.load(input_file)

    def _parse_sections(self):
        """Parse the chapters and sections they're nested in."""
        sections = self.input_file['sections']
        output = []

        next_chapter_idx = 1  # global through all sections
        for idx, ele in enumerate(sections):
            if type(ele) == str:
                if ele.startswith(UNNUMBERED_MARK):
                    c = Chapter(name=ele[len(UNNUMBERED_MARK):])
                else:
                    c = Chapter(name=ele, number=next_chapter_idx)
                    next_chapter_idx += 1
                output.append(c)
            elif type(ele) == dict:
                section_chapters = []            
                for idx2, chapter in enumerate(ele['chapters']):
                    c = Chapter(name=chapter, number=next_chapter_idx)
                    next_chapter_idx += 1
                    section_chapters.append(c)

                s = Section(name=ele['name'], chapters=section_chapters)
                output.append(s)

        return output

    def _parse_title_block(self):
        """Parse title, subtitle, and author(s)."""
        title = self.input_file['title']
        subtitle = self.input_file['subtitle']
        authors_input = self.input_file['authors']
        authors = [Author(i['name'], i['url']) for i in authors_input]

        return TitleBlock(title=title, subtitle=subtitle, authors=authors)

    def parse(self):
        """Parse all of the sections."""
        title_block = self._parse_title_block()
        section_list = self._parse_sections()
        toc = TableOfContents(section_list)
        notes = Notes(section_list)

        return Outline(title_block=title_block, table_of_contents=toc, notes=notes)


class MarkdownWriter(object):
    """Write native objects into a notes file in markdown format."""

    def __init__(self, outline):
        self.outline = outline

    def _write_author(self):
        """Output a single author."""
        pass

    def _write_title_block(self):
        """Output the title, subtitle, and authors."""
        pass

    # def _write_section_toc(self):
    #     """Output a section for the table of contents."""
    #     pass

    # def _write_section_outline(self):
    #     """Output a section for the outline."""
    #     pass

    # def _write_chapter_toc(self):
    #     """Output a chapter for the table of contents."""
    #     pass

    # def _write_chapter_outline(self):
    #     """Output a chapter for the outline."""
    #     pass

    def _write_table_of_contents(self):
        """Output the formatted table of contents."""
        pass

    def _write_outline(self):
        """Output the formatted outline portion of the entire document."""
        pass

    def _write_title_block(self):
        """Output the formatted title block."""
        pass

    def write(self, output_file):
        """Output the entire file."""
        title_block = self.outline.title_block
        toc = self.outline.table_of_contents
        notes = self.outline.notes

        output_elements = [title_block, toc, notes]
        output_str = '\n\n---\n\n'.join([str(i) for i in output_elements])
        output_file.write(output_str)


# def locate_indices(elements):
#     """
#     Find and return indices which split the top-level book chapters/sections into three groups.

#     They are: (1) pre-chapters, (2) numbered chapters, and (3) post-chapters. Pre-chapters are
#     unnumbered sections at the beginning (e.g., Preface). Numbered chapters are the normal ones
#     (e.g., Chapter 1). Post-chapters are unnumbered sections at the end (e.g., Aferword).

#     Assumptions:
#     - pre- and post-chapters aren't nested
#     - sections are always unnumbered
#     """

#     pre_idx, numbered_idx, post_idx = [None] * 3  # indices

#     # Are there pre-chapters?
#     first = elements[0]
#     if is_unnumbered(first) and is_chapter(first):
#         pre_idx = 0

#     for idx, ele in enumerate(elements):
#         if is_chapter(ele):
#             if not numbered_idx and is_numbered(ele):
#                 numbered_idx = idx
#         elif is_section(ele):
#             chapters_in_section = ele['chapters']
#             for idx2, chapter in enumerate(chapters_in_section):
#                 if not numbered_idx and is_numbered(chapter):
#                     numbered_idx = [idx, idx2]  # section index, chapter index

#     if type(numbered_idx) == list:
#         remaining = elements[numbered_idx[0]:]
#     elif type(numbered_idx) == int:
#         remaining = elements[numbered_idx:]

#     for idx, ele in enumerate(remaining):
#         if is_chapter(ele):
#             if not post_idx and is_unnumbered(ele):
#                 post_idx = idx + numbered_idx
#         elif is_section(ele):
#             chapters_in_section = ele['chapters']
#             for idx2, chapter in enumerate(chapters_in_section):
#                 if not post_idx and is_numbered(chapter):
#                     post_idx = [idx + numbered_idx, idx2]

#     print (pre_idx, numbered_idx, post_idx)
#     import pdb ; pdb.set_trace()

#     return (pre_idx, numbered_idx, post_idx)


# def generate_toc(chapters, pre_index, numbered_index, post_index):
#     """Return the table of contents fragment."""
#     toc = []

#     if pre_index is not None:
#         for i, chapter in enumerate(chapters[pre_index:numbered_index]):
#             title = chapter[len(UNNUMBERED_MARK):]
#             toc.append('- [{title}](#pre{number})'.format(number=i+1, title=title))

#     for i, chapter in enumerate(chapters[numbered_index:post_index]):
#         toc.append('- [{number}. {title}](#ch{number})'.format(number=i+1, title=chapter))

#     if post_index is not None:
#         for i, chapter in enumerate(chapters[post_index:]):
#             title = chapter[len(UNNUMBERED_MARK):]
#             toc.append('- [{title}](#post{number})'.format(number=i+1, title=title))

#     return '\n'.join(toc)


# def generate_sections(chapters, pre_index, numbered_index, post_index):
#     """Return the chapters fragment."""
#     sections = []

#     section_base_template = '## {section_head}\n\n- TODO\n\n<sub><sup>[back to top](#)</sub></sup>'

#     if pre_index is not None:
#         for i, chapter in enumerate(chapters[pre_index:numbered_index]):
#             pre_head_template = '<a name="pre{number}"></a>{title}'
#             title = chapter[len(UNNUMBERED_MARK):]
#             section_head_frag = pre_head_template.format(number=i+1, title=title)
#             section_frag = section_base_template.format(section_head=section_head_frag)
#             sections.append(section_frag)

#     for i, chapter in enumerate(chapters[numbered_index:post_index]):
#         numbered_head_template = '<a name="ch{number}"></a>{number}. {title}'
#         section_head_frag = numbered_head_template.format(number=i+1, title=chapter)
#         section_frag = section_base_template.format(section_head=section_head_frag)
#         sections.append(section_frag)

#     if post_index is not None:
#         for i, chapter in enumerate(chapters[post_index:]):
#             post_head_template = '<a name="post{number}"></a>{title}'
#             title = chapter[len(UNNUMBERED_MARK):]
#             section_head_frag = post_head_template.format(number=i+1, title=title)
#             section_frag = section_base_template.format(section_head=section_head_frag)
#             sections.append(section_frag)

#     return '\n\n\n'.join(sections)


def main():
    """Create the outline file from a template file."""
    args = setup()
    in_, out = args.input, args.output

    p = YAMLParser(input_file=in_)
    outline = p.parse()

    w = MarkdownWriter(outline=outline)
    w.write(output_file=out)


if __name__ == '__main__':
    main()
