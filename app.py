from flask import Flask, redirect, g, request
import psycopg2
import psycopg2.pool

app = Flask(__name__, static_folder="public", static_url_path="")


@app.route('/')
def index():
       return redirect('/index.html')


# setup database using SimpleConnectionPool
app.config['postgreSQL_pool'] = psycopg2.pool.SimpleConnectionPool(
        1,  # min number of connections
    10,  # max number of connections
    host='127.0.0.1',
    port='5432',
    database='music_library'
)

#function to get connection to the DB, use in eachroute that needs to access DB


def get_db_conn():
    if 'db' not in g:
        g.db = app.config['postgreSQL_pool'].getconn()
        print('Got connection to DB!')
        return g.db


@app.teardown_appcontext
def close_db_conn(taco):
    db = g.pop('db', None)
    if db is not None:
        app.config['postgreSQL_pool'].putconn(db)
        print('Closing connection!')

# DELETE ROUTE -- JOHN






# PUT FOR CHECK IN -- BRADY 







#get all songs

@app.route('/song', methods=['GET', 'POST']) # CASSEN HERE FOR GET AND POST
def songStuff():
    if request.method == 'GET':
        return getAllSongs()
    elif request.method == 'POST':
        return addSong(request.form )


def addSong(song):
  print('Adding song', song)
  cursor = None
  response = None
  try:
    # Get a connection, use that to get a cursor
    conn = get_db_conn()
    cursor = conn.cursor()
    # TODO Database INSERT
    sql = 'INSERT INTO songs (rank, track, artist, published) VALUES (%s, %s, %s, %s);'
    cursor.execute(sql, (song['rank'], song['track'],
                         song['artist'], song['published']))
    # IMPORTANT - FOR Add, Update, Delete - Make sure to commit!!!
    conn.commit()
    response = {'msg': 'Added song'}, 201
  # python equivalent of catch
  except psycopg2.Error as e:
    print('Error from DB', e.pgerror)
    response = {'msg': 'Error Adding song'}, 500
  # python equivalent of finally
  else:
    if cursor:
      # close the cursor
      cursor.close()
  return response

#get all songs

@app.route('/songs')
def getAllSongs():
    #get a connection, use that to get a cursor
    conn = get_db_conn()
    cursor = conn.cursor()
    #run our select query
    cursor.execute('SELECT * FROM songs ORDER BY id DESC')
    #get our results
    result = cursor.fetchall()
    #IMPORTANT! Close cursor
    cursor.close()
    # Send back results
    return {'songs': result}
