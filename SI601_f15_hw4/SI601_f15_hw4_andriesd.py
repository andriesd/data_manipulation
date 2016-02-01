# -*- coding: utf-8 -*-

import sqlite3 as sqlite
import json

con = sqlite.connect('si601hw4_andriesd.db')

input = open('movie_actors_data.txt', 'rU')
lst_of_dct = []
for line in input:
    line = line.rstrip()
    movie_data = json.loads(line)
    data_dct = {}
    data_dct['genres'] = movie_data['genres']
    data_dct['title'] = movie_data['title']
    data_dct['imdb_id'] = movie_data['imdb_id']
    data_dct['rating']= movie_data['rating']
    data_dct['actors'] = movie_data['actors']
    data_dct['year'] = movie_data['year']
    lst_of_dct.append(data_dct)

# for further breaking down tuples where second item is a list
def tuples2tuples(input, first_key, second_key):
    table = []
    for dct in input:
        tup = (dct[first_key], dct[second_key])
    #print tup
    #print len(tup[1])
        if len(tup[1]) > 1:
            for genre in tup[1]:
                newtup = (tup[0], genre)
            #print newtup
                table.append(newtup)
        else:
            newtup = (tup[0], tup[1][0])
            #print newtup
            table.append(newtup)
    return table


movie_genre_table = tuples2tuples(lst_of_dct, 'imdb_id', 'genres')

movie_table = []
for dct in lst_of_dct:
    tup = (dct['imdb_id'],dct['title'], dct['year'], dct['rating'])
    movie_table.append(tup)

movie_actor_table = tuples2tuples(lst_of_dct, 'imdb_id', 'actors')

with sqlite.connect('si601hw4_andriesd.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Movie_genre")
    cur.execute("CREATE TABLE Movie_genre (IMDB_ID INT, GENRE TEXT)")
    cur.executemany("INSERT INTO Movie_genre VALUES(?, ?)", movie_genre_table)
    cur.execute("SELECT GENRE, COUNT(IMDB_ID) AS num FROM Movie_genre GROUP BY GENRE ORDER BY num DESC LIMIT 10")
    rows = cur.fetchall()
    print 'Top Ten Genres:'
    print 'Genre, Movies'
    for row in rows:
        print row[0]+', '+str(row[1])
print '\n'

with sqlite.connect('si601hw4_andriesd.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Movies")
    cur.execute("CREATE TABLE Movies (IMDB_ID INT, TITLE TEXT, YEAR INT, RATING REAL)")
    cur.executemany("INSERT INTO Movies VALUES (?, ?, ?, ?)", movie_table)
    cur.execute("SELECT YEAR, COUNT(IMDB_ID) AS num FROM Movies GROUP BY YEAR")
    rows = cur.fetchall()
    print 'Movies broken down by year:'
    print 'Year, Movies'
    for row in rows:
        print str(row[0])+', '+str(row[1])
print '\n'

with sqlite.connect('si601hw4_andriesd.db') as con:
    cur = con.cursor()
    cur.execute("SELECT M.TITLE, M.YEAR, M.RATING FROM Movies as M JOIN Movie_genre as G ON (M.IMDB_ID=G.IMDB_ID) WHERE G.GENRE='Sci-Fi' ORDER BY M.RATING DESC, M.YEAR DESC")
    rows = cur.fetchall()
    print 'Sci-Fi Movies:'
    print 'Title, Year, Rating'
    for row in rows:
        print row[0]+', '+str(row[1])+', '+str(row[2])
print '\n'

with sqlite.connect('si601hw4_andriesd.db') as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Movie_actor")
    cur.execute("CREATE TABLE Movie_actor (IMDB_ID INT, ACTOR TEXT)")
    cur.executemany("INSERT INTO Movie_actor VALUES (?, ?)", movie_actor_table)
    cur.execute("SELECT A.ACTOR, COUNT(A.IMDB_ID) AS appeared FROM Movie_actor as A JOIN Movies as M ON A.IMDB_ID=M.IMDB_ID WHERE M.YEAR >=2000 GROUP BY A.ACTOR ORDER BY appeared DESC LIMIT 10")
    rows = cur.fetchall()
    print 'In and after year 2000, top 10 actors who played in most movies:'
    print 'Actor, Movies'
    for row in rows:
        print row[0]+', '+str(row[1])
print '\n'

with sqlite.connect('si601hw4_andriesd.db') as con:
    cur = con.cursor()
    cur.execute("SELECT A.ACTOR, COUNT(A.IMDB_ID) as appeared FROM Movie_actor AS A JOIN Movie_genre as G ON A.IMDB_ID=G.IMDB_ID WHERE G.GENRE='Comedy' GROUP BY A.ACTOR ORDER BY appeared DESC LIMIT 10")
    rows = cur.fetchall()
    print 'Top 10 actors who played in most comedy movies:'
    print 'Actor, Comedy Movies'
    for row in rows:
        print row[0]+', '+str(row[1])
print '\n'

with sqlite.connect('si601hw4_andriesd.db') as con:
    cur = con.cursor()
    cur.execute("SELECT A.ACTOR, B.ACTOR, COUNT(A.IMDB_ID) FROM Movie_actor A, Movie_actor B WHERE A.IMDB_ID=B.IMDB_ID and A.ACTOR <> B.ACTOR and A.ACTOR < B.ACTOR GROUP BY A.ACTOR, B.ACTOR HAVING COUNT(A.IMDB_ID) > 1 ORDER BY COUNT(A.IMDB_ID) DESC LIMIT 20")
    rows = cur.fetchall()
    print 'Top 20 most frequent pairs of actors who co-starred in the same movie:'
    print 'Actor A, Actor B, Co-starred Movies'
    for row in rows:
        print row[0]+', '+row[1]+', '+str(row[2])