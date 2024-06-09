import sqlite3
from database.connection import get_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'
    
     def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) <= 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def save_to_db(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO authors (id, name) VALUES (?, ?)', (self.id, self.name))
        connection.commit()
        connection.close()

    @staticmethod
    def get_author(id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (id,))
        row = cursor.fetchone()
        connection.close()
        return Author(row[0], row[1])

    def articles(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT articles.* FROM articles
        JOIN authors ON authors.id = articles.author_id
        WHERE authors.id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    def magazines(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT DISTINCT magazines.* FROM magazines
        JOIN articles ON magazines.id = articles.magazine_id
        WHERE articles.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        connection.close()
        return magazines
models/Magazine.py
python
Copy code
import sqlite3
from database.connection import get_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        self.save_to_db()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) <= 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def save_to_db(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)', (self.id, self.name, self.category))
        connection.commit()
        connection.close()

    @staticmethod
    def get_magazine(id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (id,))
        row = cursor.fetchone()
        connection.close()
        return Magazine(row[0], row[1], row[2])

    def articles(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT articles.* FROM articles
        JOIN magazines ON magazines.id = articles.magazine_id
        WHERE magazines.id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        connection.close()
        return articles

    def contributors(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT DISTINCT authors.* FROM authors
        JOIN articles ON authors.id = articles.author_id
        WHERE articles.magazine_id = ?
        ''', (self.id,))
        contributors = cursor.fetchall()
        connection.close()
        return contributors

    def article_titles(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT title FROM articles
        WHERE magazine_id = ?
        ''', (self.id,))
        titles = cursor.fetchall()
        connection.close()
        return [title[0] for title in titles] if titles else None

    def contributing_authors(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT authors.* FROM authors
        JOIN articles ON authors.id = articles.author_id
        WHERE articles.magazine_id = ?
        GROUP BY authors.id
        HAVING COUNT(articles.id) > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        connection.close()
        return authors if authors else none
