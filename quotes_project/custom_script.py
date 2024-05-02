import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_project.settings")

django.setup()

from quotes.models import Author, Quote
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM authors")
    authors_from_database = cursor.fetchall()

    cursor.execute("SELECT * FROM quotes")
    quotes_from_database = cursor.fetchall()


def migrate_data_from_postgres():
    print("Подключение к базе данных...")

    try:
        authors_from_database = Author.objects.all()
        quotes_from_database = Quote.objects.all()
    except Exception as e:
        print("Ошибка подключения к базе данных:", str(e))
        return

    print("Подключение к базе данных успешно!")

    authors_data = []
    for author in authors_from_database:
        author_data = {
            "fullname": author.fullname,
            "born_date": author.born_date,
            "born_location": author.born_location,
            "description": author.description
        }
        authors_data.append(author_data)

    quotes_data = []
    for quote in quotes_from_database:
        tags = quote.tags
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',')]
        tags = "{" + ",".join(tags) + "}"
        quote_data = {
            "quote": quote.quote,
            "author_fullname": quote.author_fullname,
            "tags": tags
        }
        quotes_data.append(quote_data)
    print(authors_data)
    print(quotes_data)
    for author_data in authors_data:
        fullname = author_data['fullname']
        born_date = author_data['born_date']
        born_location = author_data['born_location']
        description = author_data['description']

        print(f"Добавление данных автора: {fullname}...")

        try:
            print(author_data)
            Author.objects.create(
                fullname=fullname,
                born_date=born_date,
                born_location=born_location,
                description=description
            )
            print(f"Данные автора {fullname} успешно добавлены!")
        except Exception as e:
            print(f"Ошибка при добавлении данных автора {fullname}: {str(e)}")

    for quote_data in quotes_data:
        quote = quote_data['quote']
        author_fullname = quote_data['author_fullname']
        tags = quote_data['tags']

        print(f"Добавление цитаты: {quote}...")

        try:
            print(quote_data)
            Quote.objects.create(
                quote=quote,
                author_fullname=author_fullname,
                tags=tags
            )
            print(f"Цитата {quote} успешно добавлена!")
        except Exception as e:
            print(f"Ошибка при добавлении цитаты {quote}: {str(e)}")


migrate_data_from_postgres()
