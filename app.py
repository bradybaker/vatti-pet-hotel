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
    database='pet_hotel'
)

# function to get connection to the DB, use in eachroute that needs to access DB


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

# Route parameters - id will pass in the id of the pet to be deleted
# this is DELETE
@app.route('/pets/<id>', methods=["DELETE"])
def delete_pet(id):
    print('Terminating furbaby', id)
    cursor = None
    response = None
    try:
        # Get a connection
        conn = get_db_conn()
        # use connection to get a cursor
        cursor = conn.cursor()
        # set up delete command syntax
        sql = 'DELETE from pets WHERE id = %s;'
        # execute delete commmand on database passing in id
        cursor.execute(sql, (id))
        # need to commit or bad things
        conn.commit()
        response = ({'msg': 'Terminated pet.'}, 201)
        # catch errors
    except psycopg2.Error as e:
        print('Error from DB', e.pgerror)
        response = {'msg': 'Error terminating pet magic'}, 500
    else:
        if cursor:
            # close the cursor
            cursor.close()
        if conn:
            # close the cursor
            close_db_conn(response)
    return response


# PUT FOR CHECK IN -- BRADY
@app.route('/pets/<id>', methods=['PUT'])
def changeCheckInStatus(id):
    print('Changing check-in status of fur baby with id of', id)
    cursor = None
    response = None
    try:
        conn = get_db_conn
        cursor = conn.cursor()
        sql = '''UPDATE pets SET checked_in = 'No' where id=%s;'''
        cursor.execute(sql, (id))
        conn.commit()
        response = ({'msg': 'Changed check-in status.'}, 200)
    except psychopg2.Error as e:
        print('Error from DB', e.pgerror)
        response = {'msg': 'Error changing the check-in status'}, 500
    else:
        if cursor:
            cursor.close()
        if conn:
            close_db_conn(response)
    return response


@app.route('/pets', methods=['GET', 'POST'])  # CASSEN HERE FOR GET AND POST
def petStuff():
    if request.method == 'GET':
        return getAllPets()
    elif request.method == 'POST':
        return addPet(request.form)


def addPet(pet):
    print('Adding pet', pet)
    cursor = None
    response = None
    try:
        # Get a connection, use that to get a cursor
        conn = get_db_conn()
        cursor = conn.cursor()
        # Database INSERT
        sql = 'INSERT INTO pets ("pet", "breed", "color") VALUES (%s, %s, %s);'
        cursor.execute(sql, (pet['pet'], pet['breed'], pet['color']))
        # Commit
        conn.commit()
        response = {'msg': 'Added pet magic'}, 201
        # Catch
    except psycopg2.Error as e:
        print('Error from DB', e.pgerror)
        response = {'msg': 'Error Adding more pet magic'}, 500
    else:
        if cursor:
            # close the cursor
            cursor.close()
    return response


@app.route('/pets')
def getAllPets():
    # get a connection, use that to get a cursor
    conn = get_db_conn()
    cursor = conn.cursor()
    # run our select query
    cursor.execute('SELECT * FROM pets ORDER BY checked_in DESC;')
    result = cursor.fetchall()
    cursor.close()
    # get our results
    return {'pets': result}
