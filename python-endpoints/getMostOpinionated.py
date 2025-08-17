import sqlite3
import json

if __name__ == "__main__":
    try:
        conn = sqlite3.connect()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT source, AVG(rating) as avg_rating
        FROM articles
        GROUP BY source
        ORDER BY avg_rating
        LIMIT 5;''')

        bottomSources = list(cursor.fetchall())
        bottomSourceObjects = []  
        for source in bottomSources:
            bottomSourceObjects.append({"title": source[0], "rating": source[1]})

        if len(bottomSources) > 0:
            print(json.dumps({"Status": 200, "Message": "Got top sources", "sources": bottomSourceObjects}))
        else:
            raise Exception("Bleh belh no sources found")
    except Exception as e:
        print("Error bluhblublu")