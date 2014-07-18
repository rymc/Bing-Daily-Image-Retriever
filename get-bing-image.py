#!/usr/bin/python
import urllib2
import os
import sys
import shutil
import argparse

from xml.dom import minidom


def main(save_location):
    bing_url = 'http://www.bing.com'
    xml_url = 'http://www.bing.com/hpimagearchive.aspx?format=json&idx=0&n=1&mbl=1&mkt=en-ww'

    xml = urllib2.urlopen(xml_url)
    xml_doc = minidom.parse(xml)
    url_base = xml_doc.getElementsByTagName('urlBase')[0].firstChild.nodeValue
    extension = xml_doc.getElementsByTagName('url')[0].firstChild.nodeValue.split('.')[-1]
    image_url = bing_url + url_base + '_1920x1200.' + extension

    try:
        img = urllib2.urlopen(image_url)
    except urllib2.HTTPError as e:
        print(e)
        sys.exit(-1)

    image_name = image_url.split('/')[-1]

    if not os.path.exists(save_location):
        os.makedirs(save_location)

    if save_location[-1] != '/' or save_location[-1] != '\\':
        save_location += '/'

    with open(save_location + image_name, 'wb') as f:
        shutil.copyfileobj(img, f)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description='Download todays Bing image.')
    parser.add_argument('-d', '--dir', dest='save_location', action='store',
                        default=script_dir,
                        help='Directory to store the downloaded image (default: directory of this program)')

    results = parser.parse_args()

    main(results.save_location)

