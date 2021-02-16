import configparser
import logging
import os
import re
import sys
from datetime import date
from time import sleep

import pandas as pd
import urllib3
import xlsxwriter

from scraper import *
from text_parser import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    config = configparser.ConfigParser()
    config.read("src\config.ini", encoding="utf-8")

    page_url = first_query_page(crime=config["FILTER"]['CRIME'],
                                place=config["FILTER"]["PLACE"],
                                path=config["WEB_DRIVER"]["PATH"])
    try:
        article_data = pd.DataFrame()
        page_num = 1
        while True:
            if page_num <= int(config["FILTER"]["PAGE_LIMIT"]):
                page_content = get_bs4_content(url=page_url)

                # get all links of articles of the page
                article_urls = [
                    f'https://law.judicial.gov.tw/FJUD/{node.get("href")}'
                    for node in page_content.body.table.find_all("a", {"id": "hlTitle"})
                ]

                for num, article_url in enumerate(article_urls):
                    start_time = time.time()
                    article_num = num + 1
                    content = get_bs4_content(url=article_url)
                    main_text = get_main_text(content=content)
                    full_text = get_full_text(content=content)
                    article_id = article_num + (page_num - 1) * 20
                    row = pd.DataFrame({
                        'id': article_id,
                        'page_num': page_num,
                        'article_num': article_num,
                        'url': article_url,
                        'main_text': main_text,
                        'full_text': full_text
                    }, index=[0])
                    article_data = article_data.append(row, ignore_index=True)
                    time.sleep(0.5)
                    end_time = time.time()
                    logging.info(
                        f"page: {page_num}, ID: {article_id}, Time consumption: {(end_time - start_time):.2f} seconds")

                    # get next_page_url and assign to page_url
                    next_page_qurl = page_content.find(
                        "a", {"class": "page", "id": "hlNext"}).get("href")
                    page_url = f"https://law.judicial.gov.tw{next_page_qurl} & ot = in"
                page_num += 1
                logging.info(f"There are {len(article_data)} articles so far.")
            else:
                break

    except AttributeError as e:
        logging.error(f"error message: {e}")
        logging.error("No next_page. Stop iterating")

    project_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    query_date = date.today().strftime("%Y%m%d")
    file_prefix = f'{config["FILTER"]["CRIME"]}_{config["FILTER"]["TERM"]}_{config["FILTER"]["PLACE"]}'
    data_path = os.path.join(
        project_dir, f"../data/raw/{file_prefix}_{query_date}.xlsx")

    with pd.ExcelWriter(data_path) as writer:
        article_data.to_excel(
            writer, index=False, header=True, encoding="utf_8_sig", engine='xlsxwriter')

    report = article_data

    report['parsed_reparations'] = report['full_text'].apply(lambda x: get_parsed_result(
        text=x, regex=config["PARSING_REGEX"]['REPARATION']))

    report['parsed_words'] = report['full_text'].apply(lambda x: get_parsed_result(
        text=x, regex=config["PARSING_REGEX"]['WORD']))

    report['price'] = report['parsed_reparations'].apply(
        lambda reparation_list: char_to_number(reparation_list[0]) if reparation_list else 0)

    report['swear_isin'] = report['parsed_words'].apply(
        lambda words: any([config["FILTER"]['TERM'] in word for word in words]))

    if sum(report['swear_isin']):
        avg_price_of_swear = round(
            sum(report['price'])/sum(report['swear_isin']), 0)
        avg_string = f"costs_NTD {avg_price_of_swear}"
    else:
        avg_string = 'no_records'
    report_path = os.path.join(
        project_dir, f"../reports/{file_prefix}_{avg_string}_{query_date}.xlsx")
    with pd.ExcelWriter(report_path) as writer:
        report.to_excel(writer, index=False, header=True,
                        encoding="utf_8_sig", engine='xlsxwriter')


if __name__ == '__main__':
    main()
