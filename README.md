# Scrape Articles and Atom Feed

## Description

This project aims to scrape all the articles data from a specified url, and
then produce an atom feed, saving it into a local file.


### Dependencies

 - Python 3.6


### Install

To build the docker image:

```
docker build --tag scrap-and-atom-feed build .
```

### Usage
To run the docker image passing a cli argument:

```
docker run scrap-and-atom-feed -u [url]
```

And then you will find the correspondant .xml atom feed in the directory 'atom_feeds'.

The filename has a structure 'atom_[MAIN_URL_TITLE]_[UPDATED DATE].xml', where MAIN_URL_TITLE
is the title extracted by newspaper3k from the main url and UPDATED_DATE is the date of feed's last
update, basically a datetime.now().


### Tests

To thest the main file (from the root folder):

```
python -m unittest tests/test_main.py 
```