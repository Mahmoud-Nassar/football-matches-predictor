from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

MonthsMarketValue = ['2017-09-01', '2017-10-01', '2017-11-01', '2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01',
                     '2018-05-01', '2018-06-01']


def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = session.get(url)
    # return the soup
    return bs(html.content, "html.parser")


def get_all_tables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table")


def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers


def get_table_rows(table, header):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                if len(td.text.strip()) > 0:
                    cells.append(td.text.strip())
        if len(cells) == len(header):
            rows.append(cells)
    return rows


def save_as_csv(table_name, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")


def fetch_data(url, year):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    # tables = get_all_tables(soup)
    tables = soup.find_all("table", {"class": "items"})[:1]
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        # get all the rows of the table
        rows = get_table_rows(table, headers)
        # save table as csv file

        table_name = f"DR-{year}"
        print(f"[+] Saving {table_name}")

        save_as_csv(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\LaLiga-Players-'+table_name, headers, rows)


def main(url, idx):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    # tables = get_all_tables(soup)
    tables = soup.find_all("table", {"class": "items"})[:1]
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        # get all the rows of the table
        rows = get_table_rows(table, headers)
        # save table as csv file

        table_name = f"MV-{MonthsMarketValue[idx][5:7]}"
        print(f"[+] Saving {table_name}")
        if MonthsMarketValue[idx][2:4] == '17':
            save_as_csv(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\LaLiga-Teams-'+table_name+'-17', headers, rows)
        else:
            save_as_csv(r'C:\Users\Asus\PycharmProjects\AI_Project\dataSet\LaLiga-Teams-' + table_name+'-18', headers, rows)


def team_market_value_url_reader():
    for m, date in enumerate(MonthsMarketValue):
        try:
            u = r'https://www.transfermarkt.com/laliga/marktwerteverein/wettbewerb/ES1/stichtag/date'
            main(u, m)
        except IndexError:
            print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
            exit(1)


def disciplinary_record_per_year(y):
    try:
        u = r'https://www.transfermarkt.com/laliga/suenderkartei/wettbewerb/ES1/saison_id/2017'
        fetch_data(u, y)
    except IndexError:
        print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
        exit(1)


if __name__ == '__main__':
    disciplinary_record_per_year(2017)
