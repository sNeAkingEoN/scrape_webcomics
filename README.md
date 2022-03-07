# Scrape Webcomics

This scraper is written to scrape simple webcomics hosted on individual sites (e.g. through Hiveworks), not on plattforms like Tapas. It is part of my digital humanities master's thesis.

## Requirements

Libraries needed
python 3.8.10
pandas <= 1.4.1 
scrapy <= 2.6.1

This Scraper was last tested on Ubuntu 20.04.

## Installation and Usage

To use this scraper, simply clone it into a directory of your choice. A good idea is `/home/<username>/SRC`.

Take a look at `settings.py`, ideally chose another user agent and check the `DATA_BASE_DIRECTORY` setting. The scraper should work out of the box. To start crawling, enter `scrapy crawl <name-of-spider, e.g. witchy>`.
If you want to write a spider for a webcomic of your choice, it's best to derive it from the base class `FromStartSpider`. The `JOBDIR` setting makes sure to save the crawls (including metadata) in case of a keyboard interrupt via CTRL+C.