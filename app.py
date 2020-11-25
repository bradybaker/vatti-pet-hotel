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
        return addPet(request.form )


def addPet(pet):
  print('Adding pet', pet)
  cursor = None
  response = None
  try:
    # Get a connection, use that to get a cursor
    conn = get_db_conn()
    cursor = conn.cursor()
    # Sql text to insert pets into the table
    sql = 'INSERT INTO pets ("pet", "breed", "color") VALUES (%s, %s, %s);'
    cursor.execute(sql, (pet['pet'], pet['breed'], pet['color']))
    # Commit
    conn.commit()
    response = {'msg': 'Added a pet'}, 201
  # Do catch
  except psycopg2.Error as e:
    print('Error from DB', e.pgerror)
    response = {'msg': 'Error adding your pet'}, 500
  else:
    if cursor:
      # Close the cursor
      cursor.close()
  return response


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
