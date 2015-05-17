"""
All of the data containers.
"""

class Author(object):
    def __init__(self, name, url=None):
        self.name = name
        self.url = url

    def __str__(self):
        return '[{name}]({url})'.format(name=self.name, url=self.url) if self.url else self.name


class TitleBlock(object):
    def __init__(self, title, subtitle, authors):
        self.title = title
        self.subtitle = subtitle
        self.authors = authors

    def __str__(self):
        s = '# {title}\n*{subtitle}*<br>\nby {authors}'.format(title=self.title, subtitle=self.subtitle,authors=', '.join([str(a) for a in self.authors]))
        return s


class Section(object):
    def __init__(self, name, chapters):
        self.name = name
        self.chapters = chapters

    def __str__(self):
        return '{}'.format(self.name)


class Chapter(object):
    def __init__(self, name, number=None):
        self.name = name
        self.number = number

    def __str__(self):
        if self.number is not None:
            s = '{}. {}'.format(self.number, self.name)
        else:
            s = '{}'.format(self.name)
        return s


class TableOfContents(object):
    def __init__(self, sections):
        self.sections = sections

    def __str__(self):
        s = '**Table of Contents**\n\n'
        for ele in self.sections:
            if type(ele) is Chapter:
                s += '- {}\n'.format(ele)
            elif type(ele) is Section:
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
            if type(ele) is Chapter:
                s += '## {name}\n\n- TODO\n\n'.format(name=str(ele))
            elif type(ele) is Section:
                s += '## {name}\n\n'.format(name=str(ele))
                for c in ele.chapters:
                    s += '### {name}\n\n- TODO\n\n'.format(name=str(c))
        return s


class Outline(object):
    """The whole thing!"""

    def __init__(self, title_block, table_of_contents, notes):
        self.title_block = title_block
        self.table_of_contents = table_of_contents
        self.notes = notes
