import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import csv
from openai import OpenAI


load_dotenv()
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")
THE_NEWS_APIKEY = os.getenv("THE_NEWS_APIKEY")

client = OpenAI(api_key=OPENAI_APIKEY)

def get_website_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    content = requests.get(url, headers=headers, timeout=10).content

    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')

    return soup.get_text()

def classify_opinionation(input):
    response = client.responses.create(
        model = "gpt-5-mini",
        input = f"""You are an expert news analyst. Your task is to analyze the news articles and classify its level of opinionation on a scale of 1 to 5.

        INPUT INSTRUCTIONS:
        - **1** You will be provided an scraper page which will include adds and other articles. THE ARTICLE IS THE MOST COHERENT AND LONGEST PASSAGE IN THE INPUT.

        OUTPUT INSTRUCTIONS:
        Use the following scale for your classification:
        - **1 (Most Opinionated):** The article is an editorial, op-ed, or pure commentary. It uses emotional, persuasive, or biased language and presents opinions as facts. The author's viewpoint is central to the piece.
        - **2 (Fairly Opinionated):** The article is a news analysis or feature that, while based on facts, is framed to support a specific viewpoint. It may lack balance and use subjective language.
        - **3 (Mixed / Slightly Opinionated):** The article is primarily a news report but contains some subjective language, unbalanced quotes, or a subtle authorial tone that hints at a bias.
        - **4 (Mostly Factual):** The article is a standard, objective news report. It focuses on reporting events, uses neutral language, and attributes opinions directly to named sources.
        - **5 (Strictly Factual):** The article is purely informational, like a wire report or data summary. It contains no discernible opinion, emotional language, or bias.

        Analyze the article below and respond with a single integer (1, 2, 3, 4, or 5) and nothing else.

        **INPUT**:

        {input}
        """
    )

    return response.output_text



if __name__ == "__main__":
    for i in range(95):
        try:
            newsApiLink = f"https://api.thenewsapi.com/v1/news/all?language=en&limit=3&page={i+1}categories=science,business,tech,politics&exclude_categories=general,sports,health,entertainment,food,travel&api_token={THE_NEWS_APIKEY}"
            response = requests.get(newsApiLink)

            #Just to make sure
            if response.status_code != 200:
                raise Exception(f"Sorry the api didn't work {response.status_code} {response.content}")
            
            articles = response.json()["data"]

            fields = []
            for article in articles:
                title = article["title"].replace(","," ")
                description = article["description"].replace(","," ")
                source = article["source"]
                url = article["url"]

                content = "Could not scrape content." 
                try:
                    print(f"Scraping content from: {url}")
                    content = get_website_content(url).replace("\n"," ").replace("\t", " ").replace(","," ")
                except Exception as e:
                    print(f"Error scraping {url}: {e}")

                rating = -1
                try: 
                    print(f"Generating rating for article {title}")
                    if (content != "Could not scrape content."):
                        rating = classify_opinionation(content)
                except Exception as e:
                    print(f"OpenAI API ran into exception {e}")

                fields.append([title, description, source, url, content, rating])

            with open("./scraper-to-train/scraped.csv", 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(fields)

        except Exception as e:
            print(f"error dumbass: {e}")
            break
