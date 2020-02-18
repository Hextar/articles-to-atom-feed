import sys
import argparse
import newspaper
import nltk
import uuid 
from argparse import ArgumentParser
from newspaper import news_pool
from newspaper import Article
from feedgen.feed import FeedGenerator
from datetime import datetime


# IT: https://www.costasmeralda.it/in-spiaggia-con-gli-amici-a-quattro-zampe/
# EN: https://www.nytimes.com/column/learning-article-of-the-day

# A Class of support representing an Atom Entry
class Entry:
	id = ''
	title = ''
	link = ''
	updated = ''

	def __init__(self,  link, title): 
		self.id = uuid.uuid1().hex
		self.title = title
		self.link = link
		self.updated = datetime.now().isoformat()+'Z'


def main():
	try:	
		parser = ArgumentParser()
		parser.add_argument("-u", "--url", dest="url", help="url of the articles to be parse")
		args = parser.parse_args()

		if (args.url == None):
			print('ERROR ARGUMENT PARSING: an url argument is required')
		return args.url

	except Exception as e:
		print('ERROR, ARGUMENT PARSING: ', e)


def scrapeAllUrls(url):
	try:
		url_list = list()

		# Instantiate newspaper object
		url_paper = newspaper.build(url, memoize_articles=False)

		# Activate newspaper multi-threading
		papers = [url_paper]
		news_pool.set(papers, threads_per_source=4)
		news_pool.join()

		# Append the articles found in the url
		for article in url_paper.articles:
			url_list.append(article.url)

		return url_list
			
	except Exception as e:
		print('ERROR, SCRAPE URL LIST: ', e)


def scrapeArticle(url):
	try:
		# Instantiate the article object
		article = Article(url)

		# Download the article
		article.download()

		# Parse the article
		article.parse()

		# Natural Language Processing
		article.nlp()

		entry = Entry(url, article.title)

		return entry

	except Exception as e:
		print('ERROR, SCRAPE ARTICLE DETAILS: ', e)


def createAtomFeed(main_entry, entries):
	# Instantiate Feed Generator object
	fg = FeedGenerator()
	fg.id(main_entry.id)
	fg.title(main_entry.title)
	fg.link(href=main_entry.link, rel='alternate')	
	fg.updated(main_entry.updated)

	for entry in entries:
		if (entry and isinstance(entry, Entry)):
			# Append an entry to the feed
			fe = fg.add_entry()
			fe.id(entry.id)
			fe.title(entry.title)
			fe.link(href=entry.link, rel='alternate')
			fe.updated(entry.updated)
	
	
	# Write the ATOM feed to a file
	fg.atom_file('atom.xml') 
		

if __name__ == "__main__":
	argument_url = main()
	entries = list()
	url_list = list()
	title = ''

	if (argument_url):

		main_entry = scrapeArticle(argument_url)

		# Get all article urls in the url
		url_list = scrapeAllUrls(argument_url)

		if (url_list != None):
			for url in url_list:
				entries.append(scrapeArticle(url))
				
		if (entries != None):
			createAtomFeed(main_entry, entries)

	
