"""
Service for gathering data from sources (restcountries rn) and saving it in DB
BTW it's possible to simply use python lib "python-restcountries",  but it's not the goal of this test project
As a future improvments it's possible to take out crawler, parser, loader to separte files,
create folders for custom scripts for crawlers and parsers for differ data sources
create some conventions for data fileds and what could go to the DB
"""

from typing import Any, Dict, List

import pandas as pd
import requests

from core.db import engine
from core.settings import settings


class Scraper:
    """
    Class as main interfase for service.
    """

    def __init__(self, source: str, fields: List[str] = None):
        self.source = source  # could be 'restcountries' only for now
        self.fields = fields or []

    def scrape(self) -> Any:
        match self.source:
            case "restcountries":
                # could be pick out to the script or yaml (what ever way/lib you choose) file for each data source
                crawler = Crawler(self.fields)
                raw_data = crawler.crawl()

                df = Parser.parse_json_restcountries(raw_data)

                Loader.save_df_psql(self.source, df)
                return df

            case "local_json":
                ...
            case _:
                raise ValueError(f"Unknown source: {self.source}")


class Crawler:
    """
    Fetching data
    a.t.m. it's nerrowed to gather data from https://restcountries.com/v3.1/all.
    """

    def __init__(self, fields: List[str] = None):
        self.fields = fields or []

    def crawl(self):
        params = {"fields": ",".join(self.fields)} if any(self.fields) else {}
        response = requests.get(settings.BASE_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()


class Parser:
    """
    Transform data (json from the request a.t.m.) to the pandas DataFrame format.
    Some data validations and parsing other data sources in the future(?)
    """

    @staticmethod
    def parse_json_restcountries(data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert JSON to pandas DataFrame.
        """

        # here is a possible place for calling validate function (need to add it in Parser class)
        df = pd.json_normalize(data, sep="_")

        # duno if it's ok for you to have such custom solutions, but without these optiomisations there is > 700 columns, that is unusable 
        # as i mentioned before it's possble to rewrite class so it calls script for data source to optimize data
        patterns = [
            r"name_nativeName_\w+_official",
            r"name_nativeName_\w+_common",
            r"currencies_\w+_name",
            r"currencies_\w+_symbol",
            r"languages_\w+",
        ]

        for column_regex in patterns:
            common_columns = df.filter(regex=column_regex).columns
            if len(common_columns) == 0:
                continue

            new_name = column_regex.replace(r"_\w+", "")
            df[new_name] = df[common_columns].apply(lambda row: ", ".join(row.dropna().astype(str)), axis=1)
            df.drop(columns=common_columns, inplace=True)

        return df  # pd.json_normalize(data, sep='_')


class Loader:
    """
    Saving data to the psql. possible to update with other data storages
    """

    @staticmethod
    def save_df_psql(source_name: str, data: pd.DataFrame):
        data.to_sql(name=source_name, con=engine, if_exists="append")


if __name__ == "__main__":
    print(Scraper("restcountries", settings.DEFAULT_FIELDS).scrape())  # First step test
