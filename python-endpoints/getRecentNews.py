import sqlite3
import json

db_file = "../python-endpoints/articles.db"

if __name__ == "__main__":
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''SELECT * from articles
                    WHERE recent = TRUE''')
        
        sources = list(cursor.fetchall())
        recentSources = []

        for source in sources:
            title = source[0]
            description = source[1]
            sourceName = source[2]
            url = source[3]
            content = source[4]
            rating = source[5]

            sourceJSON = {"title": title, "description": description, "source": sourceName, "url": url, "content": content, "rating": rating}
            recentSources.append(sourceJSON)

        if len(sources) > 0:
            print(json.dumps({'Status': 200, 'Message': "Got most recent articles", "news": recentSources}))
            conn.close()
        else:
            raise Exception("There are 0 recent articles")
    except Exception as e:
        print(json.dumps({'Status': 500, 'Message': str(e), "news": []}))
        conn.close()



