import pymysql.cursors
from music_logger import app
from os.path import abspath
from sys import argv

# Sets paths for mock SQL files
groupsTableFile = abspath('./test/seeds/music_logger_groups.sql')
tracksTableFile = abspath('./test/seeds/music_logger_tracks.sql')
groupsDataFile = abspath('./test/data/groups_data.sql')
tracksDataFile = abspath('./test/data/tracks_data.sql')

# Sets up connection to database
connection = pymysql.connect(host=app.config.get("DB_HOST"),
                             user=app.config.get("DB_USER"),
                             password=app.config.get("DB_PASSWORD"),
                             db=app.config.get("DB_NAME"),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def create(args):
    if any(x in args for x in ['-h', '--help']):
        print_help()
        return
    if any(x in args for x in ['-s', '--seed']):
        seed_tracks()
        return
    try:
        if any(x in args for x in ['-e', '--erase']):
            with connection as cur:
                cur.execute('DROP DATABASE IF EXISTS music_logger;')
                cur.execute('CREATE DATABASE music_logger;')
            connection.commit()
            return
        read_sql_file(connection, groupsTableFile)
        read_sql_file(connection, tracksTableFile)
        read_sql_file(connection, groupsDataFile)
    finally:
        connection.close()


def print_help():
    """
    Prints help statement for file usage
    :return: None
    """
    print("\nUsage:\n  dbsetup [options]\n")
    print("Options:\n  -e, --erase\t\tResets the database 'music_logger' with no tables initialized\n"
          "  -s, --seed\t\tAdds track data into the database")


def seed_tracks():
    """
    Populates tracks table with mock data
    :return: None
    """
    try:
        read_sql_file(connection, tracksDataFile)
    finally:
        connection.close()


def read_sql_file(connect, file):
    """
    Helper function to read mock SQL files
    :param connect: Connection to Database
    :param file: SQL file to read
    :return: None
    """
    with connect.cursor() as cursor:
        with open(file) as f:
            for x in f.read().strip().split(';'):
                x.strip()
                if x != '':
                    cursor.execute(x)
    connection.commit()


# Converts argv to lowercase for better user input parsing
arguments = [element.lower() for element in argv]

# Calls main function
create(arguments)
