import sqlite3
import json

db_file = "articles.db"

if __name__ == "__main__":
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''SELECT * from articles
                    WHERE recent = TRUE''')
        
        result = list(cursor.fetchall())

        if len(result) > 0:
            print(json.dumps({'Status': 200, 'Message': "Got most recent articles", "news": result}))
            conn.close()
        else:
            raise Exception("There are 0 recent articles")
    except Exception as e:
        print(json.dumps({'Status': 500, 'Message': e, "news": result}))
        conn.close()



