import ast
import logging
import os
import urllib.request

from bs4 import BeautifulSoup


def main():
    # Setup logging
    logging.basicConfig(filename='example.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filemode='w', level=logging.INFO, encoding='utf-8')

    logging.info('-- Start Availability Check --')

    urls = ast.literal_eval(os.environ.get("URLS"))
    for url in urls:
        #print(url)
        page = urllib.request.urlopen(url)
        logging.info(f'Page status code: {page.status}')
        if page.status != 200:
            logging.exception(f'Page status code not 200 at {url}')
            return

        soup = BeautifulSoup(page, features='html.parser')
        # get contents of div
        result = soup.find_all("div", {"class": "availability"})
        content = result[0].text
        logging.info(content.rstrip('\n'))

        if '54: Out of stock.' not in content:
            logging.info('Available')
            exit(-1)
        else:
            logging.info('Not available')
            #exit(-1)


if __name__ == '__main__':
    main()
