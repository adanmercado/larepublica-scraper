import requests
import lxml.html as html
import os
import datetime

HOME_URL : str = 'https://www.larepublica.co/'
XPATH_LINK_QUERY : str = '//div[@class="col mb-4"]/div/text-fill/a/@href'
XPATH_TITLE_QUERY : str = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_AUTHOR_QUERY :str = '//div[@class="author-article"]/div/button/text()|//div[@class="author-article"]/div/span/text()'
XPATH_SUMMARY_QUERY : str = '//div[@class="lead"]/p/text()'
XPATH_CONTENT_QUERY : str = '//div[@class="html-content"]/p/text()|//div[@class="html-content"]/p/node()/text()'
DOWNLOAD_FOLDER = './notices'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            parser = html.fromstring(content)

            try:
                print("#" * 50)
                title = parser.xpath(XPATH_TITLE_QUERY)[0]
                if not title.startswith('"'):
                    title = f'"{title}"'
                print(f'Title: {title}')

                author = parser.xpath(XPATH_AUTHOR_QUERY)[0]
                if not author.startswith('"'):
                    author = f'"{author}"'
                print(f'Author: {author}')

                summary = parser.xpath(XPATH_SUMMARY_QUERY)[0]
                if not summary.startswith('"'):
                    summary = f'"{summary}"'
                print(f'Sumamry: {summary}')

                notice = parser.xpath(XPATH_CONTENT_QUERY)
                notice = ' '.join(notice)
                if not notice.startswith('"'):
                    notice = f'"{notice}"'

                line = ','.join([title, author, summary, notice]) + '\n'
                print("#" * 50)

                with open(os.path.join(DOWNLOAD_FOLDER, f'{today}.csv'), 'a') as f:
                    f.write(line)
            except IndexError:
                print('Index error')
                return
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def start():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            parser = html.fromstring(content)
            
            links = parser.xpath(XPATH_LINK_QUERY)

            if not os.path.exists(DOWNLOAD_FOLDER):
                os.mkdir(DOWNLOAD_FOLDER)

            today = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
            if len(links):
                with open(os.path.join(DOWNLOAD_FOLDER, f'{today}.csv'), 'w') as f:
                    f.write(','.join(['Title', 'Author', 'Summary', 'Notice']) + '\n')

            for link in links:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)