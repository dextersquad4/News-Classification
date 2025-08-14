import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import csv

load_dotenv()

THE_NEWS_APIKEY = os.getenv("THE_NEWS_APIKEY")

if __name__ == "__main__":
    try:
        # newsApiLink = f"https://api.thenewsapi.com/v1/news/headlines?locale=us&language=en&page=100&api_token={THE_NEWS_APIKEY}"
        # response = requests.get(newsApiLink)

        # #Just to make sure
        # if response.status_code != 200:
        #     raise Exception("Sorry the api didn't work")
        
        # articles = response.json()["data"]

        fields = [["title", "description", "source", "url"], ["title", "description", "source", "url"]]
        # for article in articles:
        #     title = article["title"]
        #     description = article["description"]
        #     source = article["source"]
        #     url = article["url"]

        #     data.append([title, description, source, url])

        with open("scraped.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(fields)
            





    except Exception:
        print("error dumbass")
