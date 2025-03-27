import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=quiz_app user=teacher")

# Open a cursor to perform database operations
cursor = conn.cursor()

# Execute a command: this creates a new table
# id, name, score - names of columns in DB
# integer, varchar(40) - types of columns
# all the rest (primary key, not null) - some extra options, don't worry about them
cursor.execute('''
    create table if not exists users(
        id integer primary key,
        name varchar(40) not null,
        score integer
    );
''')

# Insert data into the table
cursor.execute('''
    INSERT INTO users (id, name, score)
    VALUES(3, 'Sasha', 100500);

    INSERT INTO users (id, name, score)
    VALUES(4, 'Anya', 200600);
''')

# Commit the transaction
conn.commit()

# Query the database
cursor.execute("SELECT * FROM users")
res = cursor.fetchall()
print(type(res))
print(res)
print(type(res[0]))
print(res[1][2])

# Close the connection
cursor.close()
conn.close()
