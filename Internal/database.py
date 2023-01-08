#Global Imports
import os,sys,dotenv,colorama,asyncio,aiomysql,mysql.connector
#Specific Imports
from dotenv import load_dotenv
from colorama import Fore
#Local Imports
from . import console

load_dotenv()

def test_connection(host=os.environ['SQL_IP'],user=os.environ['SQL_Username'],password=os.environ['SQL_Password'],database=os.environ['SQL_DB']):
    try:
        connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        db=database,
        charset='utf8',
        use_unicode=True
    )
        if (connection != None):
            console.print_message("Testing Connection to SQL server",True)
            console.print_debug(f"{connection}")
            # Check the connection status
            if connection.is_connected():
                console.print_message("Connection to MySQL database successful")
            else:
                console.print_error("Connection to MySQL database failed")
    except mysql.connector.Error as error:
        console.print_error(f"Error connecting to MySQL database: {error}")

    finally:
        # Close the connection
        if connection.is_connected():
            connection.close()
            console.print_debug("MySQL connection closed")

async def createdatabase(database,host=os.environ['SQL_IP'],user=os.environ['SQL_Username'],password=os.environ['SQL_Password']):
    console.print_message(f"Creating new database '{database}'")
    connection = await aiomysql.connect(
        host=host, 
        user=user, 
        password=password, 
        charset='utf8', 
        use_unicode=True)
        
    # Create a cursor to execute queries
    cursor = await connection.cursor()
    databases = await cursor.fetchall()
    if (database) in str(databases):
        console.print_debug(f"{database} exists!")
    else:
        # Create the database
        await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        # Confirm the creation of the database
        await cursor.execute(f"SHOW DATABASES")
        databases = await cursor.fetchall()
        if (database) in str(databases):
            console.print_message(f"{database} has been created successfully")
        else:
            console.print_error(f"Error creating {database}")

    # Close the cursor and connection
    await cursor.close()
    connection.close()

async def CreateTable(table,columns,database=os.environ['SQL_DB'],host=os.environ['SQL_IP'],user=os.environ['SQL_Username'],password=os.environ['SQL_Password']):
    try:
        connection = await aiomysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            charset='utf8',
            use_unicode=True
        )
        cursor = await connection.cursor()
        await cursor.execute(f"SHOW TABLES")
        tables = cursor.fetchall()
        if (table) in str(tables):
            console.print_debug(f"{table} Exists")
        else:
            await cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns})")
            # Confirm the creation of the table
            await cursor.execute(f"SHOW TABLES")
            tables = cursor.fetchall()
            if (table) in str(tables):
                console.print_debug(f"{table} Exists")
            else:
                console.print_error(f"Error creating {table}")

        # Close the cursor and connection
        await cursor.close()
        connection.close()
    except Exception as e:
        temp = e
        console.print_error(f"{e}")

async def WriteTable(query,database,host=os.environ['SQL_IP'],user=os.environ['SQL_Username'],password=os.environ['SQL_Password']):
    connection = await aiomysql.connect(
        host=host,
        user=user,
        password=password,
        db=database,
        charset='utf8',
        use_unicode=True
    )
    console.print_debug(f"Writing Query: {query} to {database}")
    cursor = await connection.cursor()
    await cursor.execute(query)
    await connection.commit()
    await cursor.close()
    connection.close()

async def ReadTable(query,database,host=os.environ['SQL_IP'],user=os.environ['SQL_Username'],password=os.environ['SQL_Password']):
    try:
        connection = await aiomysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            charset='utf8',
            use_unicode=True
        )
    except Exception as e:
        console.print_error(f"Cannot Connect to DB: {e}")
    console.print_debug(f"Reading Query: {query} to {database}")
    cursor = await connection.cursor()
    await cursor.execute(query)
    result = await cursor.fetchall()
    await cursor.close()
    connection.close()
    if result is None:
        console.error(f"database: {database} | query: {query} has no results")
        return 0
    else:
        return result


async def ReadTableNow(query, database, host=os.environ['SQL_IP'],user=os.environ['SQL_Username'],password=os.environ['SQL_Password']):
    # Connect to the database
    conn = await aiomysql.connect(
        host=host,
        user=user,
        password=password,
        db=database,
    )

    # Create a cursor
    cur = await conn.cursor()

    # Execute the SELECT query
    await cur.execute(query)

    # Fetch all the results from the SELECT query
    rows = await cur.fetchall()

    # Close the cursor and connection
    await cur.close()
    conn.close()

    # Return the results
    return rows