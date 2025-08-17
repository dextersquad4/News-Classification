import sqlite3
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import bs4 as BeautifulSoup
import torch
from dotenv import load_dotenv
import os

load_dotenv()

THE_NEWS_APIKEY = os.getenv("THE_NEWS_APIKEY")

db_file = "articles.db"


def get_website_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    content = requests.get(url, headers=headers, timeout=10).content

    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')

    return soup.get_text()

def classify_opinionation(text):
    tokenized_input = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**tokenized_input)

    return outputs.logits.item()
        


if __name__ == "__main__":
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles(
                   title TEXT, 
                   description TEXT,
                   source TEXT,
                   url TEXT,
                   content TEXT,
                   rating float,
                   recent BOOLEAN
                   );''')
    
    cursor.execute('''UPDATE articles 
                    SET recent = FALSE
                    WHERE recent = TRUE;''')
    conn.commit()
    output_dir = "opinionation_model/checkpoint-147/"
    tokenizer = AutoTokenizer.from_pretrained(output_dir)
    model = AutoModelForSequenceClassification.from_pretrained(output_dir)



    for i in range(7):
        try:
            newsApiLink = f"https://api.thenewsapi.com/v1/news/top?language=en&limit=3&page={i+1}categories=science,business,tech,politics&exclude_categories=general,sports,health,entertainment,food,travel&api_token={THE_NEWS_APIKEY}"
            response = requests.get(newsApiLink)

            #Just to make sure
            if response.status_code != 200:
                raise Exception(f"Sorry the api didn't work {response.status_code} {response.content}")
            
            articles = response.json()["data"]

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
                    rating = classify_opinionation(title+description+content)
                except Exception as e:
                    print(f"Ran into model excpetion")


                cursor.execute("SELECT url from articles where url = ?", (url,))
                exists_row = cursor.fetchone()

                if not exists_row:
                    #Add each article to the db if the url is unique
                    cursor.execute('''INSERT INTO articles (title, description, source, url, content, rating, recent)
                                VALUES (?, ?, ?, ?, ?, ?, ?);''', (title, description, source, url, content, rating, True))
                conn.commit()

        except Exception as e:
            print(f"error dumbass: {e}")
            break
            
    conn.close()
    

    