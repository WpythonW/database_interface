import mysql.connector

class Sql:
    config = {
        'user': 'root',
        'password': 'pepkadodiko54#',
        'host': '178.216.100.196',
        'database': 'Students',
        'raise_on_warnings': True
    }

    def __init__(self):
        self.cnx = mysql.connector.connect(**self.config)
        self.cursor = self.cnx.cursor()

    def close_connection(self):
        self.cnx.close()

    def get_table(self, name):
        self.cursor.execute(f"SELECT * FROM {name};")
        columns = self.cursor.column_names
        rows = self.cursor.fetchall()
        return columns, rows

    def get_all_tables(self):
        self.cursor.execute("SHOW TABLES;")
        rows = self.cursor.fetchall()
        return rows

    def get_columns(self, name):
        self.cursor.execute(f"SHOW COLUMNS FROM {name};")
        rows = self.cursor.fetchall()
        return rows

    def change_table(self, name, field, value, new_field, new_val):
        #p_resp = 'and'.join([field[i] + '=' + value[i] for i in range(len(field))])
        self.cursor.execute(f"UPDATE {name} set {new_field} = '{new_val}' where {field} = '{value}';")
        self.cnx.commit()
        print(f"changed row, command: UPDATE {name} set {new_field} = '{new_val}' where {field} = '{value}';")

    def delete_row(self, name, field, value):
        self.cursor.execute(f"DELETE FROM {name} where {field} = '{value}';")
        self.cnx.commit()
        print(f"deleted row, command: DELETE FROM {name} where {field} = '{value}';")

    def add_row(self, name, row):
        try:
            self.cursor.execute(f"INSERT INTO {name} VALUES{row};")
        except:
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            self.cursor.execute(f"INSERT INTO {name} VALUES{row};")
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        self.cnx.commit()
        print(f"added row, command: INSERT INTO {name} VALUES({row});")
        a = 0