import unittest
from html_remover import removeHtmlTags

class TestHtmlRemover(unittest.TestCase):
    def test_remove_html_tags(self):
        self.assertEqual(removeHtmlTags('<p>Hello</p>'), 'Hello')
        self.assertEqual(removeHtmlTags('<div><p>Nested</p></div>'), 'Nested')

    def test_remove_html_tags_empty(self):
        self.assertEqual(removeHtmlTags(''), '')
        self.assertEqual(removeHtmlTags('<div></div>'), '')

    def test_remove_html_tags_no_tags(self):
        self.assertEqual(removeHtmlTags('Hello'), 'Hello')
        self.assertEqual(removeHtmlTags('Hello World'), 'Hello World')

    def test_remove_html_tags_with_parameters(self):
        self.assertEqual(removeHtmlTags('<p class="test">Hello</p>'), 'Hello')
        self.assertEqual(removeHtmlTags('<p id="test">Hello</p>'), 'Hello')
        self.assertEqual(removeHtmlTags('<p class="test" id="test">Hello</p>'), 'Hello')

if __name__ == '__main__':
    unittest.main()