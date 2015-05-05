"""
Generate the notes outline for a book.
"""

import argparse

import yaml


UNNUMBERED_MARK = '.'  # prefix to skip numbering for sections like Preface


def setup():
    """Parse command-line args."""
    parser = argparse.ArgumentParser(description='Generate the notes outline for a book.')
    parser.add_argument('input', type=argparse.FileType('r'), help='metadata and table of contents file in yaml format')
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


def locate_section_indices(input_file):
    """
    Find and return indices which split the book chapters into three sections.

    The three sections are: pre, numbered, and post chapters. Pre chapters include unnumbered
    sections at the beginning (e.g., Preface). Numbered includes standard numbered section (e.g.,
    Chapter 1). Post chapters include unnumbered sections at the end (e.g., Aferword).
    """
    pre_index = None
    numbered_index = None
    post_index = None

    first_section = input_file['sections'][0]
    if first_section.startswith(UNNUMBERED_MARK):
        pre_index = 0

    for idx, section in enumerate(input_file['sections']):
        if not section.startswith(UNNUMBERED_MARK):
            numbered_index = idx
            break

    for idx, section in enumerate(input_file['sections'][numbered_index:]):
        if section.startswith(UNNUMBERED_MARK):
            post_index = idx + numbered_index
            break

    return (pre_index, numbered_index, post_index)


def generate_toc(input_file, pre_index, numbered_index, post_index):
    """Return the table of contents fragment."""
    toc = []

    if pre_index is not None:
        for i, section in enumerate(input_file['sections'][pre_index:numbered_index]):
            title = section[len(UNNUMBERED_MARK):]
            toc.append('- [{title}](#pre{number})'.format(number=i+1, title=title))

    for i, section in enumerate(input_file['sections'][numbered_index:post_index]):
        toc.append('- [{number}. {title}](#ch{number})'.format(number=i+1, title=section))

    if post_index is not None:
        for i, section in enumerate(input_file['sections'][post_index:]):
            title = section[len(UNNUMBERED_MARK):]
            toc.append('- [{title}](#post{number})'.format(number=i+1, title=title))

    return '\n'.join(toc)


def generate_sections(input_file, pre_index, numbered_index, post_index):
    """Return the sections fragment."""
    sections = []

    section_base_template = '## {section_head}\n\n- TODO\n\n<sub><sup>[back to top](#)</sub></sup>'

    if pre_index is not None:
        for i, section in enumerate(input_file['sections'][pre_index:numbered_index]):
            section_head_template = '<a name="pre{number}"></a>{title}'
            title = section[len(UNNUMBERED_MARK):]
            section_head_frag = section_head_template.format(number=i+1, title=title)
            section_frag = section_base_template.format(section_head=section_head_frag)
            sections.append(section_frag)

    for i, section in enumerate(input_file['sections'][numbered_index:post_index]):
        section_head_template = '<a name="ch{number}"></a>{number}. {title}'
        section_head_frag = section_head_template.format(number=i+1, title=section)
        section_frag = section_base_template.format(section_head=section_head_frag)
        sections.append(section_frag)

    if post_index is not None:
        for i, section in enumerate(input_file['sections'][post_index:]):
            section_head_template = '<a name="post{number}"></a>{title}'
            title = section[len(UNNUMBERED_MARK):]
            section_head_frag = section_head_template.format(number=i+1, title=title)
            section_frag = section_base_template.format(section_head=section_head_frag)
            sections.append(section_frag)

    return '\n\n\n'.join(sections)


def main():
    """Create the outline file from a template file."""
    args = setup()
    input_file = yaml.load(args.input)

    title = generate_title(input_file)
    authors = generate_authors(input_file)
    section_indices = locate_section_indices(input_file)
    toc = generate_toc(input_file, *section_indices)
    sections = generate_sections(input_file, *section_indices)

    outline_template = '{title}\nby {authors}\n\n---\n\n**Table of Contents**\n\n{toc}\n\n---\n\n{sections}\n'
    outline = outline_template.format(title=title, authors=authors, toc=toc, sections=sections)

    with open('output.md', 'w') as output_file:
        output_file.write(outline)


if __name__ == '__main__':
    main()
