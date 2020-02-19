import unittest
import main


class TestMain(unittest.TestCase):

	def test_get_vars(self):
		parser = parse_args(['-u', '-f'])
		self.assertTrue(parser.url)
		self.assertTrue(parser.full)


	def test_scrape_all_urls(self):
		pass


	def test_scrape_article(self):
		pass


	def test_create_atom_feed(self):
		pass


if __name__ == '__main__':
	unittest.main()