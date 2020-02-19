import warnings
import unittest
from unittest.mock import patch, mock_open
from main import *


class TestMain(unittest.TestCase):

	def setUp(self):
		warnings.simplefilter('ignore', category=ImportWarning)

	def test_get_vars(self):
		url = 'https://example.com'
		parser = parse_args(['-u', url, '-f', 'False'])
		self.assertTrue(parser.url)
		self.assertEqual(parser.url, url)
		self.assertTrue(parser.full)
		self.assertEqual(parser.full, 'False')


	def test_get_vars_with_full_text(self):
		parser = parse_args(['-u', 'https://example.com', '-f', 'True'])
		self.assertTrue(parser.url)
		self.assertEqual(parser.url, 'https://example.com')
		self.assertTrue(parser.full)
		self.assertEqual(parser.full, 'True')


	def test_scrape_all_urls(self):
		url = 'https://www.nytimes.com/column/learning-article-of-the-day'
		url_list = scrape_all_urls(url)
		self.assertGreater(len(url_list), 0)


	def test_scrape_all_urls_empty(self):
		url = 'https://no-article.com'
		url_list = scrape_all_urls(url)
		self.assertEqual(len(url_list), 0)


	def test_scrape_article(self):
		url = 'https://www.nytimes.com/column/learning-article-of-the-day'
		entry = scrape_article(url)
		self.assertTrue(entry)
		self.assertTrue(entry.id)
		self.assertTrue(entry.authors)
		self.assertTrue(entry.title)
		self.assertTrue(entry.text)
		self.assertTrue(entry.summary)


	def test_scrape_article(self):
		url = 'https://no-article.com'
		entry = scrape_article(url)
		self.assertFalse(entry)


if __name__ == '__main__':
	unittest.main()