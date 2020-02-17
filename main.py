import sys
import argparse
from argparse import ArgumentParser

# https://www.costasmeralda.it/in-spiaggia-con-gli-amici-a-quattro-zampe/

def main():
	try:	
		parser = ArgumentParser()
		parser.add_argument("-u", "--url", dest="url", help="url of the articles to be parse")
		args = parser.parse_args()
		return args.url

	except Exception as e:
		print('ERROR, ARGUMENT PARSING: ', e)


def scrapeAllUrls(url):
	import newspaper

	try:
		url_list = []
		html_page = newspaper.build(url)

		for article in html_page.articles:
			print(article.url)
			url_list.append(article.url)

		# Return the articles found in the url
		return url_list
			
	except Exception as e:
		print('ERROR, SCRAPE URL LIST :', e)


def scrapeArticle(url):
	from newspaper import Article

	try:
		# Instantiate the article object
		article = Article(url)

		# Download the article
		article.download()

		# Parse the article
		article.parse()

		# Natural Language Processing
		article.nlp()

		print(article.authors)
		print(article.publish_date)
		print(article.keywords)

		print(article.text)

	except Exception as e:
		print('ERROR, SCRAPE ARTICLE DETAILS', e)


if __name__ == "__main__":
	argument_url = main()
	url_list = list()

	# Get all article urls in the url
	url_list = scrapeAllUrls(argument_url)
	print(url_list)

	for url in url_list:
		scrapeArticle(url)