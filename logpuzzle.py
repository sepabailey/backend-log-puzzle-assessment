#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
 HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
  rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

__author__ = "Sean Bailey, Koren Niles, Kano Marvel, Chelsea White, Ben Myers"

import os
import re
import sys
import argparse
import urllib
# if sys.version_info[0] >= 3:
#     from urllib.request import urlretrieve
# else:
#     from urllib import urlretrieve


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    puzzle_urls = []
    with open(filename, 'r') as log_file:
        log_list = log_file.read().split('\n')
        log_list = list(filter(lambda x: ('/puzzle/' in x), log_list))
        for url in log_list:
            url_result = re.findall(r'GET (\S+) HTTP', url)
            puzzle_urls.append(url_result[0])
    url_list = create_urls(puzzle_urls)
    url_list = list(set(url_list))
    sorted_urls = sorted(url_list, key=return_last_word)
    print(sorted_urls)
    return sorted_urls


def create_urls(urls):
    front = 'http://code.google.com'
    url_returns = [front+url for url in urls]
    # for url in urls:
    #     url = front + url
    # return url
    return url_returns


def return_last_word(url):
    return re.findall(r'-(....).jpg', url)


create_urls('animal_code.google.com')


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print('dir made')
    index_html = '<html><body>'
    for index, url in enumerate(img_urls):
        image_name = 'img' + str(index)
        print('Retrieving {}'.format(url))
        urllib.urlretrieve(url, dest_dir + '/' + image_name)
        index_html += '<img src = {}></img>'.format(image_name)
    index_html += '</body></html>'
    with open(dest_dir + '/index.html', 'w') as write_index:
        write_index.write(index_html)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    parsed_args = parser.parse_args(args)
    img_urls = read_urls(parsed_args.logfile)
    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
