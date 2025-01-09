# my_database_lib/database.py

import pyodbc
import pandas as pd


class Database:
    def __init__(self, server, database, user=None, password=None, driver='ODBC Driver 17 for SQL Server'):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.driver = driver
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            # Ha nincs megadva felhasználónév és jelszó, akkor Windows hitelesítést használunk
            if self.user and self.password:
                conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password}'
            else:
                conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'

            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            print("INFO: Connected to SQL Server")
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Unable to connect to SQL Server: {e}\033[0m")

    def insert_bulk(self, df, table):
        try:
            # Lekérdezzük a táblát az adatbázisból
            query = f"SELECT * FROM {table}"
            db_df = self.get_table(table)

            # Ha a tábla üres, akkor létrehozunk egy üres DataFrame-et
            if db_df is None:
                print(f"INFO: The table {table} does not exist or is empty.")
                return

            # Kiválasztjuk azokat az oszlopokat, amelyek megegyeznek a DataFrame-ben és az adatbázisban
            common_columns = list(set(df.columns).intersection(set(db_df.columns)))

            # Ha vannak közös oszlopok, akkor csak azokat insertáljuk
            if common_columns:
                # Kiválasztjuk azokat az oszlopokat, amelyeket insertálni szeretnénk
                columns = ', '.join(common_columns)
                placeholders = ', '.join(['?' for _ in common_columns])
                sql_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

                # Azokat az értékeket, amelyek megfelelnek a közös oszlopoknak
                values = [tuple(row[common_columns]) for row in df.itertuples(index=False, name=None)]

                # Az összes adat bulk insertálása
                self.cursor.executemany(sql_query, values)
                self.conn.commit()
                print(f"INFO: Rows from DataFrame inserted into {table} table based on matching columns")
            else:
                print("INFO: No matching columns between DataFrame and database table, skipping insert")

        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to insert DataFrame: {e}\033[0m")

    def insert_row(self, row_data, table):
        try:
            # Példa SQL insert query
            columns = ', '.join(row_data.keys())
            placeholders = ', '.join(['?' for _ in row_data])
            sql_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql_query, tuple(row_data.values()))
            self.conn.commit()
            print("INFO: Row inserted successfully")
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to insert row: {e}\033[0m")

    def update_row(self, keys, updates, table):
        try:
            # Példa SQL update query
            set_clause = ', '.join([f"{k} = ?" for k in updates])
            where_clause = ' AND '.join([f"{k} = ?" for k in keys])
            sql_query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            self.cursor.execute(sql_query, tuple(updates.values()) + tuple(keys.values()))
            self.conn.commit()
            print("INFO: Row updated successfully")
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to update row: {e}\033[0m")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            print("INFO: Query executed successfully")
            return results
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to execute query: {e}\033[0m")
            return None

    def get_table(self, table):
        try:
            query = f"SELECT * FROM {table}"
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]  # Oszlopnevek kinyerése
            rows = self.cursor.fetchall()
            table_df = pd.DataFrame.from_records(rows, columns=columns)

            print("INFO: Table fetched successfully")
            return table_df
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to fetch table: {e}\033[0m")
            return None

    def query(self, query_string):
        try:
            query = query_string
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]  # Oszlopnevek kinyerése
            rows = self.cursor.fetchall()
            table_df = pd.DataFrame.from_records(rows, columns=columns)

            print("INFO: Table fetched successfully")
            return table_df
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to fetch table: {e}\033[0m")
            return None

    def delete(self, table, primary_key=None, key_value=None):
        try:
            if primary_key and key_value:
                # Delete rows by primary key
                sql_query = f"DELETE FROM {table} WHERE {primary_key} = ?"
                self.cursor.execute(sql_query, (key_value,))
                self.conn.commit()
                print(f"INFO: Row(s) with {primary_key} = {key_value} deleted successfully")
            else:
                # If no primary key is provided, delete all rows in the table
                sql_query = f"DELETE FROM {table}"
                self.cursor.execute(sql_query)
                self.conn.commit()
                print(f"INFO: All rows in {table} deleted successfully")
        except pyodbc.Error as e:
            print(f"\033[91mERROR: Failed to delete from table: {e}\033[0m")

    def close(self):
        if self.conn:
            self.conn.close()
            print("INFO: Connection to SQL Server closed")
