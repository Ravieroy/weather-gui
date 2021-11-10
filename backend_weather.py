import sqlite3
##from tkinter.constants import SEPARATOR


def connect():
    conn=sqlite3.connect('cities.db')
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS city (id INTEGER PRIMARY KEY, name text)")
    conn.commit()
    conn.close()

def insert(name):
    conn=sqlite3.connect('cities.db')
    cur=conn.cursor()
    cur.execute("INSERT INTO city VALUES (NULL,?)", (name,))
    conn.commit()
    conn.close()

def view():
    conn=sqlite3.connect('cities.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM city")
    rows=cur.fetchall()
    conn.close()
    return [x[1] for x in rows]
    # return rows

def get_id(name=''):
    conn=sqlite3.connect('cities.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM city WHERE name=?", (name,))
    rows=cur.fetchall()
    conn.close()
    return [x[0] for x in rows]

def delete(id):
    conn=sqlite3.connect('cities.db')
    cur=conn.cursor()
    cur.execute("DELETE FROM city WHERE id=?", (id,))
    conn.commit()
    conn.close()

connect()
