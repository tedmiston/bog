"""
Test the data containers for books and outlines.
"""

import unittest

from models import Author


class AuthorModelTestCase(unittest.TestCase):
    """Test the author data container."""

    def setUp(self):
        self.name = 'Jason Fried'
        self.url = 'https://basecamp.com/'

    def test_author_blank(self):
        """Test an author that's empty."""
        self.assertRaises(ValueError, Author, name='')

    def test_author_invalid(self):
        """Test an author of the wrong data type."""
        self.assertRaises(TypeError, Author, name=5)

    def test_author_null(self):
        """Test an author that's null."""
        self.assertRaises(TypeError, Author, name=None)

    def test_url_blank(self):
        """Test a url that's empty."""
        self.assertRaises(ValueError, Author, name=self.name, url='')

    def test_url_invalid(self):
        """Test a url of the wrong data type."""
        self.assertRaises(TypeError, Author, name=self.name, url=5)

    def test_url_null(self):
        """Confirm a url that's null will pass."""
        a = Author(name=self.name, url=None)
        self.assertIsNone(a.url)

    def test_init_with_minimal_kwargs(self):
        """Test creating an author with the minimum possible set of keyword args."""
        a = Author(name=self.name)
        self.assertEqual(a.name, self.name)
        self.assertIsNone(a.url)

    def test_init_with_full_kwargs(self):
        """Test creating an author with a complete set of keyword args."""
        a = Author(name=self.name, url=self.url)
        self.assertEqual(a.name, self.name)
        self.assertEqual(a.url, self.url)

    def test_init_with_minimal_args(self):
        """Test creating an author with the minimum possible set of positional args."""
        a = Author(self.name)
        self.assertEqual(a.name, self.name)
        self.assertIsNone(a.url)

    def test_init_with_full_args(self):
        """Test creating an author with a complete set of positional args."""
        a = Author(self.name, self.url)
        self.assertEqual(a.name, self.name)
        self.assertEqual(a.url, self.url)


if __name__ == '__main__':
    unittest.main()
