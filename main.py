import sys
import argparse
from argparse import ArgumentParser
import newspaper
from newspaper import news_pool
from newspaper import Article
from werkzeug.contrib.atom import AtomFeed


# IT: https://www.costasmeralda.it/in-spiaggia-con-gli-amici-a-quattro-zampe/
# EN: https://www.nytimes.com/column/learning-article-of-the-day


def main():
	try:	
		parser = ArgumentParser()
		parser.add_argument("-u", "--url", dest="url", help="url of the articles to be parse")
		parser.add_argument("-l", "--lang", dest="language", help="url of the articles to be parse")
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
		news_pool.set(papers, threads_per_source=2)
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

		print(article.authors)
		print(article.publish_date)
		print(article.keywords)

		print(article.text)

	except Exception as e:
		print('ERROR, SCRAPE ARTICLE DETAILS: ', e)


def parseArticle():
	pass


def writeToFile():
	pass

if __name__ == "__main__":
	argument_url = main()

	if (argument_url):
		# Get all article urls in the url
		url_list = scrapeAllUrls(argument_url)
		print(url_list)

		if (url_list != None):
			for url in url_list:
				scrapeArticle(url)