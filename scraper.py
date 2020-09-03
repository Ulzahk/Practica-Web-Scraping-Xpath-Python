import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE= '//h2/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@id="proportional-anchor-1"]/div/div[@class="autorArticle" or @class="html-content"]/p[not(@class)]/text()'


def parse_new(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            new_info = response.content.decode('utf-8')
            
            parsed = html.fromstring(new_info)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                print(title)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parse = html.fromstring(home)
            links_to_news = parse.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_news)

            today = datetime.date.today().strftime('%d-%m-%y')

            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_news:
                parse_new(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()