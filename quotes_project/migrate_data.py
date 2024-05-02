import psycopg2
from pymongo import MongoClient


def migrate_data():
    mongo_client = MongoClient('mongodb+srv://maksym_sk:treka1999@cluster1.ab6kfu8.mongodb.net')
    mongo_db = mongo_client['scrape']
    mongo_authors_collection = mongo_db['author']
    mongo_quotes_collection = mongo_db['quote']

    pg_conn = psycopg2.connect(
        dbname='django_for_web',
        user='postgres',
        password='vfrc3224',
        host='localhost'
    )
    pg_cur = pg_conn.cursor()

    for author_document in mongo_authors_collection.find():
        fullname = author_document.get('fullname', '')
        born_date = author_document.get('born_date', '')
        born_location = author_document.get('born_location', '')
        description = author_document.get('description', '')

        pg_cur.execute(
            "INSERT INTO authors (fullname, born_date, born_location, description) VALUES (%s, %s, %s, %s)",
            (fullname, born_date, born_location, description)
        )

    for quote_document in mongo_quotes_collection.find():
        quote = quote_document.get('quote', '')
        author_fullname = quote_document.get('author', '')
        tags = quote_document.get('tags', [])

        pg_cur.execute(
            "INSERT INTO quotes (quote, author_fullname, tags) VALUES (%s, %s, %s)",
            (quote, author_fullname, tags)
        )

    pg_conn.commit()
    pg_cur.close()
    pg_conn.close()
    mongo_client.close()


if __name__ == "__main__":
    migrate_data()
