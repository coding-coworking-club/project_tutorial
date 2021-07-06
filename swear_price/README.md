# Swear Price

A web scraper project for investigating how much it costs when you swear words.

## Getting Started

1. Initialize a virtualenv to manage all required packages

    ```bash
    # ~/swear_price/
    pip3 install pipenv
    pipenv --python 3
    ```

2. Install packages

   Install all required packages based on `Pipfile`.

   ```bash
   # ~/swear_price/
   pipenv sync
   ```

3. Update the configaration file

    Find `src/config.ini` (in the folder named `src`) then edit it if necessary.

    - Change the default value

        - for `WEB_DRIVER` :

            Fill in your own web-driver absolute path.

        - for `FILTER` :

            Based on the format of [司法院法學資料檢索系統-裁判書查詢](https://law.judicial.gov.tw/FJUD/default_AD.aspx), `CRIME` is the keyword for "全文內容"; `PLACE` helps you choose court.

            `PAGE_LIMIT` is the maximum number of pages which will be scraped.

            After raw data is scraped, only the articles with keyword of `TERM` will be marked as "TRUE", which indicates that an article contains the swear words you interests in.

4. Execute the project

    ```bash
    # ~/swear_price/
    pipenv run python src/main.py
    ```

## Project Orginaztion

```
├── data
├── reports
├── src
│   ├── init_.py
│   ├── scraper.py
│   ├── text_parser.py
│   ├── main.py
│   └── config.ini
├── Pipfile
├── Pipfile.lock
└── README.md
```
