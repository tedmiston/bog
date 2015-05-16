"""
Generate the notes outline for a book.
"""

import argparse

import yaml


UNNUMBERED_MARK = '.'  # prefix to hide numbering on chapters like Preface
DEFAULT_OUTPUT_FILENAME = 'output.md'


def setup():
    """Parse command-line args."""
    parser = argparse.ArgumentParser(description='Generate the notes outline for a book.')
    parser.add_argument('input', type=argparse.FileType('r'), help='metadata and table of contents file in yaml format')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), required=False,
                        default=DEFAULT_OUTPUT_FILENAME,
                        help='output file name (default: %s)' % (DEFAULT_OUTPUT_FILENAME))
    args = parser.parse_args()
    return args


def generate_title(input_file):
    """Return title fragment."""
    title = input_file['title']
    subtitle = input_file['subtitle']
    return '# {title}\n*{subtitle}*<br>'.format(title=title, subtitle=subtitle)


def generate_authors(input_file):
    """
    Return authors fragment.

    Supports one or more authors, each with an optional url indicating their homepage.
    """
    authors = []

    for i in input_file['authors']:
        name = i['name']
        url = i['url']
        author = '[{name}]({url})'.format(name=name, url=url) if url else name
        authors.append(author)

    return ', '.join(authors)


def locate_section_indices(chapters):
    """
    Find and return indices which split the book chapters into three sections.

    The three sections are: pre, numbered, and post chapters. Pre chapters include unnumbered
    sections at the beginning (e.g., Preface). Numbered includes standard numbered section (e.g.,
    Chapter 1). Post chapters include unnumbered sections at the end (e.g., Aferword).
    """
    pre_index = None
    numbered_index = None
    post_index = None

    first_chapter = chapters[0]
    if first_chapter.startswith(UNNUMBERED_MARK):
        pre_index = 0

    for idx, chapter in enumerate(chapters):
        if not chapter.startswith(UNNUMBERED_MARK):
            numbered_index = idx
            break

    for idx, chapter in enumerate(chapters[numbered_index:]):
        if chapter.startswith(UNNUMBERED_MARK):
            post_index = idx + numbered_index
            break

    return (pre_index, numbered_index, post_index)


def generate_toc(chapters, pre_index, numbered_index, post_index):
    """Return the table of contents fragment."""
    toc = []

    if pre_index is not None:
        for i, chapter in enumerate(chapters[pre_index:numbered_index]):
            title = chapter[len(UNNUMBERED_MARK):]
            toc.append('- [{title}](#pre{number})'.format(number=i+1, title=title))

    for i, chapter in enumerate(chapters[numbered_index:post_index]):
        toc.append('- [{number}. {title}](#ch{number})'.format(number=i+1, title=chapter))

    if post_index is not None:
        for i, chapter in enumerate(chapters[post_index:]):
            title = chapter[len(UNNUMBERED_MARK):]
            toc.append('- [{title}](#post{number})'.format(number=i+1, title=title))

    return '\n'.join(toc)


def generate_sections(chapters, pre_index, numbered_index, post_index):
    """Return the chapters fragment."""
    sections = []

    section_base_template = '## {section_head}\n\n- TODO\n\n<sub><sup>[back to top](#)</sub></sup>'

    if pre_index is not None:
        for i, chapter in enumerate(chapters[pre_index:numbered_index]):
            pre_head_template = '<a name="pre{number}"></a>{title}'
            title = chapter[len(UNNUMBERED_MARK):]
            section_head_frag = pre_head_template.format(number=i+1, title=title)
            section_frag = section_base_template.format(section_head=section_head_frag)
            sections.append(section_frag)

    for i, chapter in enumerate(chapters[numbered_index:post_index]):
        numbered_head_template = '<a name="ch{number}"></a>{number}. {title}'
        section_head_frag = numbered_head_template.format(number=i+1, title=chapter)
        section_frag = section_base_template.format(section_head=section_head_frag)
        sections.append(section_frag)

    if post_index is not None:
        for i, chapter in enumerate(chapters[post_index:]):
            post_head_template = '<a name="post{number}"></a>{title}'
            title = chapter[len(UNNUMBERED_MARK):]
            section_head_frag = post_head_template.format(number=i+1, title=title)
            section_frag = section_base_template.format(section_head=section_head_frag)
            sections.append(section_frag)

    return '\n\n\n'.join(sections)


def main():
    """Create the outline file from a template file."""
    args = setup()

    input_file = yaml.load(args.input)
    chapters = input_file['chapters']

    title = generate_title(input_file)
    authors = generate_authors(input_file)
    section_indices = locate_section_indices(chapters)
    toc = generate_toc(chapters, *section_indices)
    chapters = generate_sections(chapters, *section_indices)

    outline_template = '{title}\nby {authors}\n\n---\n\n**Table of Contents**\n\n{toc}\n\n---\n\n{chapters}\n'
    outline = outline_template.format(title=title, authors=authors, toc=toc, chapters=chapters)

    args.output.write(outline)


if __name__ == '__main__':
    main()
