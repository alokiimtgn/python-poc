#!/usr/bin/python
import flask
from flask import request, jsonify
import sqlite3
 
from response import response

app = flask.Flask(__name__)
app.config["DEBUG"] = True
databaseName = "books.db"

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
def getAllBooks():
    conn = sqlite3.connect(databaseName)
    conn.row_factory = dict_factory
    print(dict_factory)
    cur = conn.cursor()
    try:
        all_books = cur.execute('SELECT * FROM books;').fetchall()
        #print(all_books)
        return jsonify(all_books)
    except Exception as msg:
        print(msg)  
        return jsonify(msg)  
    finally:
        #conn.close()
        #cur.close() 
        print("close")   
    

#api for fetching all the existing books on the basis of supplied params
@app.route('/api/v1/resources/books', methods=['GET'])
def getBooksBy():
    conn = sqlite3.connect('books.db')
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
def addBook():
    rmsg = ""
    conn = sqlite3.connect(databaseName) #create connectio with db
    query_parameters = request.args #get params from request
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')
    title = query_parameters.get('title')
    first_sentence = query_parameters.get('first_sentence')
    sqlQuery = "INSERT INTO books (id,author,first_sentence,published,title) values (?,?,?,?,?)"
    try:
        cur = conn.cursor()
        c = cur.execute(sqlQuery, ([id,published,author,title,first_sentence]))
        rmsg = "Record Created successfully"
    except sqlite3.IntegrityError as msg:
        rmsg = "Record already exist with this ID"
        print(msg)
    except Exception as msg:
        print(msg)    
    finally:
        conn.commit()
        conn.close()              
    return jsonify(rmsg)


#api for updating a record
@app.route('/api/v1/resources/books/updateBook', methods=['PUT'])
def updateBook():
    conn = sqlite3.connect(databaseName) #create connection with db
    cur = conn.cursor()
    query_parameters = request.args #get params from request
    sqlQuery = "UPDATE BOOKS SET first_sentence = ? , author = ? WHERE published = ?"
    if query_parameters:
        published = query_parameters.get('published')
        first_sentence = query_parameters.get("first_sentence") 
        author = query_parameters.get("author") 
        print(published)
        print(first_sentence) 
    try:
         x = cur.execute(sqlQuery,([first_sentence,author,published])); #executinng the specified curd operation
         print(x)
    except Exception as errorMessage:
         print(errorMessage)
    conn.commit()
    # print(response.function())
    print ("Records updated successfully");
    return response.sendResponse(published)


#api for deleting a record
@app.route('/api/v1/resources/books/deleteBook', methods=['DELETE'])
def deleteBook():
    conn = sqlite3.connect(databaseName) #create connection with db
    query_parameters = request.args #get params from request
    sqlQuery = "DELETE from BOOKS WHERE published = ?"
    if query_parameters:
        published = query_parameters.get('published')
    try:
        if published:
            x = conn.execute(sqlQuery,([published])); #executinng the specified curd operation
            print(x)
            if x:
                conn.commit()
                print ("Records deleted successfully");        
        conn.close()
    except Exception as errorMessage:
        print(errorMessage)
    return response.sendResponse(published) 


@app.route('/api/v1/resources/books/addEmpPrep', methods=['POST'])
def prepS():
    con = sqlite3.connect('a.db')
    cur = con.cursor()
    query_parameters = request.args
    sqlQuery = "INSERT INTO EMP (name) values (?)"
    name = query_parameters.get("name")
    print(cur.rowcount)
    #c = cur.execute('INSERT INTO EMP (name) values (?)', ([name]))
    c = cur.execute(sqlQuery,([name]))
    print(cur.rowcount)
    con.commit()
    con.close()
    return response.sendResponse("Record inserted successfully")


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()