from cassandra.cluster import Cluster


def init_db(session, keyspace_name):

    replication_settings = {
        'class': 'SimpleStrategy',
        'replication_factor': 3
    }

    # Create the keyspace
    create_keyspace_query = f"""
        CREATE KEYSPACE IF NOT EXISTS {keyspace_name}
        WITH replication = {str(replication_settings)};
    """

    session.execute(create_keyspace_query)

    # Use the created keyspace
    session.set_keyspace(keyspace_name)

    # Define the table schema
    create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_table (
            id INT PRIMARY KEY,
            name TEXT,
            weather TEXT,
            description TEXT,
            temperature FLOAT,
            feels_like FLOAT,
            humidity FLOAT,
            pressure FLOAT,
            country TEXT
        );
    """

    session.execute(create_table_query)
