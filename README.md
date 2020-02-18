# Scrape Articles and Atom Feed

## Description

This project aims to scrape all the articles data from a specified url, and
then produce an atom feed, saving it into a local file.


### Dependencies

 - Python 3.6


### Install

```
docker image -t scrap-and-atom-feed build .
```


### Usage


```
docker run --rm scrap-and-atom-feed -u [url]
```

