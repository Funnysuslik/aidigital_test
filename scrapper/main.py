'''
Service for gathering data from sources (restcountries rn) and saving it in DB
BTW it's possible to simply use python lib "python-restcountries",  but it's not the goal of this test project
'''
from typing import Any, List, Dict


import requests
import pandas as pd


from core.settings import settings


class Scraper():
  '''
  Class as main interfase for service.
  '''
  def __init__(self, source: str, fields: List[str] = None):
    self.source = source  # could be 'restcountries' only for now
    self.fields = fields or []

  def scrape(self) -> List[Dict[str, Any]]:
    match self.source:
      case "restcountries":
        crawler = Crawler(self.fields)
        raw_data = crawler.crawl()

        df = Parser.parse_json(raw_data)
        ...
        return df

      case "local_json":
        ...
      case _:
        raise ValueError(f"Unknown source: {self.source}")

    

class Crawler():
  '''
  Fetching data
  a.t.m. it's nerrowed to gaver datafrom https://restcountries.com/v3.1/all.
  '''
  def __init__(self, fields: List[str] = None):
    self.fields = fields or []


  def crawl(self):
    params = {"fields": ",".join(self.fields)} if any(self.fields) else {}
    response = requests.get(settings.BASE_API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


class Parser():
  '''
  Transform data (json from the request a.t.m.) to the pandas DataFrame format.
  Some validations(?)
  '''

  @staticmethod
  def parse_json(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert JSON to pandas DataFrame.
    Example fields: name, population, flags, region, etc.
    """
    return pd.json_normalize(data)


class Loader():
  '''
  Saving data to the psql. possible to update with other data storages
  '''
  ...


if __name__ == '__main__':
  scraper = Scraper('restcountries', settings.DEFAULT_FIELDS)
  data = scraper.scrape()
  print(data)