#!/usr/bin/python
import flask
from flask import request, jsonify
import sqlite3
 
from response import response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        print(d)
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


#api for fetching all the existing books
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    return jsonify(all_books)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


#api for fetching all the existing books on the basis of supplied params
@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')
    query = "SELECT * FROM books WHERE"
    to_filter = []
    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)
    query = query[:-4] + ';'
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)


#api for creating record
@app.route('/api/v1/resources/books/addBook', methods=['POST'])
def create_records():
    conn = sqlite3.connect('books.db') #create connectio with db
    query_parameters = request.args #get params from request
    published = query_parameters.get('published')
    print ("Opened database successfully");
    conn.execute("INSERT INTO books (author,first_sentence,published,title) \
      VALUES ('Alok', 'first_sentence', 2012, 'mytitle')"); #executinng the specified curd operation
    conn.commit()
   # print(response.function())
    print ("Records created successfully");
    return response.sendResponse(published)


#api for updating a record
@app.route('/api/v1/resources/books/updateBook', methods=['PUT'])
def update_records():
    conn = sqlite3.connect('books.db') #create connectio with db
    query_parameters = request.args #get params from request
    published = query_parameters.get('published')
    print ("Opened database successfully "+published);
    print(published)
    sql = "UPDATE BOOKS SET first_sentence = 'Canyon 1236' WHERE published = '2013'"
    x = conn.execute(sql); #executinng the specified curd operation
    print(x)
    conn.commit()
    # print(response.function())
    print ("Records updated successfully");
    return response.sendResponse(published) 

    #api for deleting a record
@app.route('/api/v1/resources/books/deleteBook', methods=['DELETE'])
def delete_records():
    conn = sqlite3.connect('books.db') #create connectio with db
    query_parameters = request.args #get params from request
    published = query_parameters.get('published')
    print ("Opened database successfully "+published);
    print(published)
    sql = "DELETE from BOOKS WHERE published = '2014'"
    x = conn.execute(sql); #executinng the specified curd operation
    print(x)
    conn.commit()
    conn.close()
    # print(response.function())
    print ("Records deleted successfully");
    return response.sendResponse(published) 
app.run()