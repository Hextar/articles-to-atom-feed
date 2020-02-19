import os
import sys
import argparse
import newspaper
import nltk
import validators
import logging
from argparse import ArgumentParser
from newspaper import news_pool
from newspaper import Article
from feedgen.feed import FeedGenerator
from model.entry import Entry


# Example of url to be scraped
# IT: https://www.costasmeralda.it/in-spiaggia-con-gli-amici-a-quattro-zampe/
# EN: https://www.nytimes.com/column/learning-article-of-the-day


# Creating the logger
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def parse_args(args):
	try:	
		parser = ArgumentParser()

		# Argument for the url to be scraped
		parser.add_argument("-u", "--url", dest="url", help="url of the articles to be parse")
		
		# Argument boolean to decide if full text need to be added to the atom feed
		parser.add_argument("-f", "--full", dest="full", help="full text in content")
		
		return parser.parse_args(args)

	except Exception as e:
		logger.error('ARGUMENT PARSING: ', e)


def scrape_all_urls(url):
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
		logger.error('SCRAPE URL LIST: ', e)


def scrape_article(url):
	try:
		# Instantiate the article object
		article = Article(url)

		# Download the article
		article.download()

		# Parse the article
		article.parse()

		# Natural Language Processing
		article.nlp()

		authors = article.authors if article.authors else ''
		title = article.title if article.title else ''
		text = article.text if article.text else ''
		summary = article.summary if article.summary else ''

		# Create the Entry
		entry = Entry(url, authors, title, text, summary)

		return entry

	except Exception as e:
		logger.error('SCRAPE ARTICLE DETAILS: ', e)


def create_atom_feed(main_entry, entries, full_content=False):
	# Instantiate Feed Generator object
	fg = FeedGenerator()
	fg.id(main_entry.link)
	fg.title(main_entry.title)
	fg.link(href=main_entry.link, rel='alternate')	
	fg.updated(main_entry.updated)

	# For each article found in the url scraped
	# extract the article metadata
	for entry in entries:
		if (entry and isinstance(entry, Entry)):

			# Append an entry to the feed only if it has an auothr
			# Cause otherwise it will cause the feed to be invalid
			if (entry.authors and len(entry.authors)):
				fe = fg.add_entry()
				fe.id(entry.link)
				for author in entry.authors:
					fe.author(name=author)
				fe.title(entry.title)
				fe.link(href=entry.link, rel='alternate')
				fe.updated(entry.updated)
				if (full_content):
					fe.content(entry.text)
				if (entry.summary):
					fe.summary(entry.summary)
	
	# Write the ATOM feed to a file
	fg.atom_file('./atom_feeds/atom_' + main_entry.title.replace(' ', '_').lower() + '_' + main_entry.updated + '.xml') 
		

if __name__ == "__main__":
	entries = list()
	url_list = list()
	title = ''

	# Get the CLI arguments
	parser = parse_args(sys.argv[1:])
	argument_url = parser.url
	full_content = parser.full == 'True' or parser.full == 'true'

	# If an url is passed
	if (argument_url and validators.url(argument_url)):

		# Get the metadatas of the main url
		main_entry = scrape_article(argument_url)

		# Get all article urls in the url
		url_list = scrape_all_urls(argument_url)

		if (url_list != None):
			for url in url_list:
				# Get the metadatas of the url
				entries.append(scrape_article(url))
				
		if (entries != None):
			create_atom_feed(main_entry, entries, full_content)

	elif (argument_url):
		logger.error('ARGUMENT PARSING: the specified argument is not a valid urpl')
	
	else:
		logger.error('ARGUMENT PARSING: an url argument is required')

	
