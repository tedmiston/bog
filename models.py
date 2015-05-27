"""
All of the data containers related to books and outlines.
"""

class Author(object):
    """The person who wrote the book and their presence on the interwebs."""

    def __init__(self, name, url=None):
        if not isinstance(name, str):
            raise TypeError
        if len(name) == 0:
            raise ValueError

        if not isinstance(url, str) and url is not None:
            raise TypeError
        if isinstance(url, str) and len(url) == 0:
            raise ValueError

        self.name = name
        self.url = url

    def __str__(self):
        return '[{name}]({url})'.format(name=self.name, url=self.url) if self.url else self.name


class TitleBlock(object):
    """The book title, subtitle, and authors."""

    def __init__(self, title, subtitle, authors):
        self.title = title
        self.subtitle = subtitle
        self.authors = authors

    def __str__(self):
        authors_str = ', '.join([str(a) for a in self.authors])
        return '# {title}\n*{subtitle}*<br>\nby {authors}'.format(title=self.title,
                                                                  subtitle=self.subtitle,
                                                                  authors=authors_str)


class Section(object):
    """A portion of the book containing chapters."""

    def __init__(self, name, chapters):
        self.name = name
        self.chapters = chapters

    def __str__(self):
        return '{}'.format(self.name)


class Chapter(object):
    """One book chapter."""

    def __init__(self, name, number=None):
        self.name = name
        self.number = number

    def __str__(self):
        number_str = '{}. '.format(self.number) if self.number else ''
        return '{}{}'.format(number_str, self.name)


class TableOfContents(object):
    def __init__(self, sections):
        self.sections = sections

    def __str__(self):
        s = '**Table of Contents**\n\n'
        for ele in self.sections:
            if isinstance(ele, Chapter):
                s += '- {}\n'.format(ele)
            elif isinstance(ele, Section):
                s += '- {}\n'.format(ele)
                for c in ele.chapters:
                    s += '  - {}\n'.format(c)
        return s.strip()


class Notes(object):
    def __init__(self, sections):
        self.sections = sections

    def __str__(self):
        s = ''
        for ele in self.sections:
            if isinstance(ele, Chapter):
                s += '## {name}\n\n- TODO\n\n'.format(name=str(ele))
            elif isinstance(ele, Section):
                s += '## {name}\n\n'.format(name=str(ele))
                for c in ele.chapters:
                    s += '### {name}\n\n- TODO\n\n'.format(name=str(c))
        return s


class Outline(object):
    """A container for all parts of the book outline."""

    def __init__(self, title_block, table_of_contents, notes):
        self.title_block = title_block
        self.table_of_contents = table_of_contents
        self.notes = notes
