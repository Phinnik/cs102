import requests
from bs4 import BeautifulSoup
import random
import time
from typing import List
import logging

class HNParser:
    def __init__(self, proxies_file: str, logfile: str, output_file: str) -> None:
        self.url = 'https://news.ycombinator.com/'
        logging.basicConfig(filename=logfile, level=logging.INFO)
        logging.info('Creating parser, horey!')
        self.get_proxies(proxies_file)
        self.current_proxy = self.proxies[-1]
        self.output_file = output_file

    def get_proxies(self, file_name: str) -> None:
        # gets proxy from file
        proxies = []
        with open(file_name) as file_handler:
            for line in file_handler:
                proxies.append(line.replace('\n', ''))
        self.proxies = proxies
        logging.info('Got proxies from {}, tere are {} proxies'.format(file_name, len(proxies)))

    def change_current_proxy(self) -> None:
        # chenges proxy
        if len(self.proxies) > 1:
            self.proxies.pop(-1)
            self.current_proxy = self.proxies[-1]
            logging.info('Changed current_proxy to {}. There are {} proxies more'.format(self.current_proxy, len(self.proxies)))
            return self.current_proxy
        else:
            logging.error('All proxies are used')
            raise Exception('All proxies are used')

    def get_page(self, appendix: str='') -> BeautifulSoup:
        # gets page if possible, else changes proxy
        try:
            logging.info('___Geting page with appendix: {}'.format(appendix))
            r = requests.get(self.url + appendix, proxies={'https':self.current_proxy})
            page = BeautifulSoup(r.text, 'html.parser')
            return page
        except Exception:
            logging.error('something wrong')
            self.change_current_proxy()
        
    def extract_next_page(self, page: BeautifulSoup) -> BeautifulSoup:
        ''' returns next page of given news personalisation page '''
        logging.info('Extracting next page')
        next_page_appendix = page.findAll('a', {'class': 'morelink'})[0].get('href')
        next_page = self.get_page(next_page_appendix)
        return next_page

    def extract_news(self, page: BeautifulSoup):
        # extracts news personalisation data
        logging.info('extracting news personalisation')
        news_table = page.findAll('table')[2]
        table_rows = news_table.findAll('tr')
        news_list = []
        for i in range(30):
            block = table_rows[i*3: i*3+3]
            author = block[1].findAll('a', {'class': 'hnuser'})[0].text
            comments = block[1].findAll('a')[-1].text
            comments = 0 if (comments == 'discuss') else comments.split(' ')[0]
            points = block[1].findAll('span', {'class': 'score'})[0].text.split(' ')[0]
            title = block[0].findAll('a', {'class': 'storylink'})[0].text
            url = block[0].findAll('a', {'class': 'storylink'})[0]['href']
            news_list.append({'author': author,
                              'comments': comments,
                              'points': points,
                              'title': title,
                              'url': url,
                              'label':''})
        return news_list

    def save_data(self, data_list: List):
        # saves data
        with open(self.output_file, 'a') as f:
            for data in data_list:
                f.write(str(data) + '\n')

    def get_news(self, n_pages: int, start_appendix: str='newest'):
        news = []
        page = self.get_page(start_appendix)
        while n_pages > 0:
            print(n_pages)

            page_news = self.extract_news(page)
            self.save_data(page_news)
            news.extend(page_news)
            page = self.extract_next_page(page)
            n_pages -= 1
            time.sleep(random.randint(1,3))

        return news


def main():
    hnp = HNParser('proxies.txt', 'logs.txt', 'data.txt')
    news = hnp.get_news(14, 'newest?next=18539297&n=841')
    print(len(news))


if __name__ == '__main__':
    main()