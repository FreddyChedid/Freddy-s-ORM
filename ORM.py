import pymysql

class ORM:
    def __init__(self, db_config, table_name):
        self._db_config = db_config
        self._table_name = table_name
        self._conn = None

    def _connect(self):
        if self._conn is None:
            self._conn = pymysql.connect(**self._db_config)

    def _disconnect(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _execute(self, query, args=None):
        self._connect()
        cursor = self._conn.cursor()
        cursor.execute(query, args)
        self._conn.commit()
        result = cursor.fetchall()
        cursor.close()
        self._disconnect()
        return result

    def select_all(self):
        query = f"SELECT * FROM {self._table_name}"
        return self._execute(query)

    def select_by_id(self, id):
        query = f"SELECT * FROM {self._table_name} WHERE id = %s"
        return self._execute(query, (id,))

    def insert(self, data):
        columns = ",".join(data.keys())
        values = ",".join(["%s"] * len(data))
        query = f"INSERT INTO {self._table_name} ({columns}) VALUES ({values})"
        
        columns_query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self._table_name}'"
        columns_data_types = {column_name: data_type for (column_name, data_type) in self._execute(columns_query)}
        
        for column_name, value in data.items():
            column_data_type = columns_data_types[column_name]
            if column_data_type.startswith("int") and not isinstance(value, int):
                print(f"Error: {value} is not an integer, expected type {column_data_type}")
            elif column_data_type.startswith("float") and not isinstance(value, float):
                print(f"Error: {value} is not a float, expected type {column_data_type}")
            elif column_data_type.startswith("varchar") and not isinstance(value, str):
                print(f"Error: {value} is not a string, expected type {column_data_type}")
        
        return self._execute(query, tuple(data.values()))

    def delete_by_id(self, id):
        query = f"DELETE FROM {self._table_name} WHERE id = %s"
        return self._execute(query, (id,))

    def truncate(self):
        query = f"TRUNCATE {self._table_name}"
        return self._execute(query)

    def select_where(self, condition, args):
        query = f"SELECT * FROM {self._table_name} WHERE {condition}"
        return self._execute(query, args)

    def update_where(self, condition, data, args):
        set_values = ",".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {self._table_name} SET {set_values} WHERE {condition}"

        
        columns_query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self._table_name}'"
        columns_data_types = {column_name: data_type for (column_name, data_type) in self._execute(columns_query)}
        for column_name, value in data.items():
            column_data_type = columns_data_types[column_name]
            if column_data_type.startswith("int") and not isinstance(value, int):
                print(f"Error: {value} is not an integer, expected type {column_data_type}")
            elif column_data_type.startswith("float") and not isinstance(value, float):
                print(f"Error: {value} is not a float, expected type {column_data_type}")
            elif column_data_type.startswith("varchar") and not isinstance(value, str):
                print(f"Error: {value} is not a string, expected type {column_data_type}")

        return self._execute(query, tuple(data.values()) + args)


    def delete_where(self, condition, args):
        query = f"DELETE FROM {self._table_name} WHERE {condition}"
        return self._execute(query, args)

    def create_table(self, columns):
        columns_str = ",".join([f"{name} {dtype}" for name, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {self._table_name} ({columns_str})"
        return self._execute(query)

    def alter_table_add_column(self, column_name, data_type):
        query = f"ALTER TABLE {self._table_name} ADD COLUMN {column_name} {data_type}"
        return self._execute(query)

    def drop_table(self):
        query = f"DROP TABLE IF EXISTS {self._table_name}"
        return self._execute(query)

    def describe_table(self):
        query = f"DESCRIBE {self._table_name}"
        return self._execute(query)

    def grant_permission(self, user, permission):
        query = f"GRANT {permission} ON {self._table_name} TO {user}"
        return self._execute(query)

    def revoke_permission(self, user, permission):
        query = f"REVOKE {permission} ON {self._table_name} FROM {user}"
        return self._execute(query)

    def join(self, table2, join_condition, columns=None):
        if columns is None:
            columns = f"{self._table_name}.*, {table2}.*"
        else:
            columns = ', '.join(columns)
        query = f"SELECT {columns} FROM {self._table_name} JOIN {table2} ON {join_condition}"
        return self._execute(query)

    def union(self, table2, columns='*', all=False):
        if all:
            query = f"SELECT {columns} FROM {self._table_name} UNION ALL SELECT {columns} FROM {table2}"
        else:
            query = f"SELECT {columns} FROM {self._table_name} UNION SELECT {columns} FROM {table2}"
        return self._execute(query)

    def order_by(self, column, order='ASC'):
        query = f"SELECT * FROM {self._table_name} ORDER BY {column} {order}"
        return self._execute(query)

    def group_by(self, columns, having=None):
        if isinstance(columns, str):
            columns = [columns]
        columns_str = ', '.join(columns)
        query = f"SELECT {columns_str} FROM {self._table_name} GROUP BY {columns_str}"
        if having is not None:
            query += f" HAVING {having}"
        return self._execute(query)

    def distinct(self, columns=None):
        if columns is None:
            columns = "*"
        else:
            columns = ', '.join(columns)
        query = f"SELECT DISTINCT {columns} FROM {self._table_name}"
        return self._execute(query)

    def limit(self, num_rows, offset=0):
        query = f"SELECT * FROM {self._table_name} LIMIT {num_rows} OFFSET {offset}"
        return self._execute(query)

    def create_index(self, index_name, columns):
        columns_str = ', '.join(columns)
        query = f"CREATE INDEX {index_name} ON {self._table_name} ({columns_str})"
        self._execute(query)

    def set_value(self, column, value, condition=None):
        if condition is None:
            query = f"UPDATE {self._table_name} SET {column} = %s"
            self._execute(query, (value,))
        else:
            query = f"UPDATE {self._table_name} SET {column} = %s WHERE {condition}"
            self._execute(query, (value,))

    def show_indexes(self):
        query = f"SHOW INDEX FROM {self._table_name}"
        return self._execute(query)

    def replace(self, id, data):
        columns_query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self._table_name}'"
        columns_data_types = {column_name: data_type for (column_name, data_type) in self._execute(columns_query)}

        for column_name, value in data.items():
            column_data_type = columns_data_types[column_name]
            if column_data_type.startswith("int") and not isinstance(value, int):
                print(f"Error: {value} is not an integer, expected type {column_data_type}")
            elif column_data_type.startswith("float") and not isinstance(value, float):
                print(f"Error: {value} is not a float, expected type {column_data_type}")
            elif column_data_type.startswith("varchar") and not isinstance(value, str):
                print(f"Error: {value} is not a string, expected type {column_data_type}")

        columns = ",".join(data.keys())
        values = ",".join(["%s"] * len(data))
        query = f"REPLACE INTO {self._table_name} (id,{columns}) VALUES (%s,{values})"
        return self._execute(query, tuple([id] + list(data.values())))


    def insert_into_select(self, columns, select_query):
        columns_str = ', '.join(columns)
        query = f"INSERT INTO {self._table_name} ({columns_str}) {select_query}"
        return self._execute(query)






