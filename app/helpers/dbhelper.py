import threading, psycopg2
from sqlalchemy import create_engine



class DbManager:
    def __init__(self, dbParams):
        self._lock = threading.Lock()
        try:
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**dbParams)

            self.cursor = self.connection.cursor()

            print('PostgreSQL database version:')
            self.cursor.execute('SELECT version()')

            db_version = self.cursor.fetchone()
            print(db_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def __del__(self):
        self.connection.close()
        print('Database connection closed!')

    def updateUserTable(self, updateData):
        
        query = f"""
        UPDATE users
        SET oncar = {updateData.onCar}
        WHERE email = '{updateData.loginData.email}'
        """

        self.cursor.execute(query)
        self.connection.commit()

        print(f"Columns updated {self.cursor.rowcount}")
        
        if self.cursor.rowcount is 0:
            return 0