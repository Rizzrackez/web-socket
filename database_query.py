import psycopg2


# It connects to the database, executes the specified request,
# and returns the data that the database provides. If the query returns no data, returns None.
def query_pg(query):
    data = None
    database_connection = psycopg2.connect("dbname='your database' user='your user' password='user password'")
    database_cursor = database_connection.cursor()
    database_cursor.execute(query) #'SELECT * FROM messages_schemas.messages;'
    try:
        data = database_cursor.fetchall()
    except:
        pass
    database_connection.commit()
    database_cursor.close()
    database_connection.close()

    return data


# Accepts list consisting of tuples.
# The first element attaches to the 'Name: ' the second to the 'Message: ', each tuple is separated by the <br> tag.
# All this is written to a string type variable and returns it.
def parse_dbData(data):
    flag = 0
    new_data = ''
    for cortege in data:
        for elem in cortege:
            if flag == 0:
                new_data += f'<br>Name: {elem}<br>'
                flag = 1
            else:
                new_data += f'Message: {elem}<br>'
                flag = 0

    return new_data


# Calls function 'query_pg' to query the database to display all the data from the table 'messages'.
# Saves this to a data variable and calls the 'parse_date' function to parse this data.
# Returns a string with HTML tags and data from table 'messages'.
def get_all_messages():
    data = query_pg('SELECT * FROM messages_schemas.messages;')
    data = parse_dbData(data)
    return (f'''
    <!doctype html>

    <html lang="en">
    <head>
      <meta charset="utf-8">
    </head>

    <body>
      <h1>All messages!</h1>
      <p>{data}</p>
    </body>
    </html>

    ''')


# Accepts an HTTP request. Parses HTTP request to take data from 'Form data'.
# Calls the 'query_pg' function to make a request to insert data into a database.
def insert_data(request):
    parsed = request.split(' ')
    parsed = parsed[-1].split('\r\n\r\n')
    name, message = parsed[-1].split('&')
    name = name.split('=')[1].replace('+', ' ').replace('%2F', '/')\
        .replace('%3F', '?')\
        .replace('%3D', '=')\
        .replace('%26', '&').\
        replace('%25', '#')
    message = message.split('=')[1].replace('+', ' ').replace('%2F', '/')\
        .replace('%3F', '?')\
        .replace('%3D', '=')\
        .replace('%26', '&').\
        replace('%25', '#')
    query_pg('INSERT INTO messages_schemas.messages ("user", user_message) VALUES (\'{}\', \'{}\');'.format(name, message))