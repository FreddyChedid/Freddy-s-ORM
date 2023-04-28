#orm code documentation
This markdown file explains the usage of the ORM (Object-Relational Mapping) code which is a Python class that helps interact with relational databases using object-oriented programming.

Requirements
This code requires the installation of pymysql Python package. The package can be installed using pip:
pip install pymysql

Usage
Creating an ORM object
To use this ORM class, you need to create an instance of the class by passing the database configuration and table name to the constructor.

For example, to create an ORM object for a table named "users" in a MySQL database with the following configuration:

makefile
Copy code
from orm import ORM

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "db": "mydb"
}

table_name = "users"

orm = ORM(db_config, table_name)
Selecting Data
The ORM object provides several methods for selecting data from the database.

To select all rows from the table, you can use the select_all() method:

makefile
Copy code
rows = orm.select_all()
To select a row by its ID, you can use the select_by_id(id) method:

makefile
Copy code
row = orm.select_by_id(1) #We are reading the record where id=1
Inserting Data
To insert data into the table, you can use the insert(data) method. The method takes a dictionary of column names and values as input. For example:

sql
Copy code
  table_name = 'mytable' 
  orm = ORM(db_config, table_name) 
  # define the data to be inserted as a dictionary
  data = {'name': 'Freddy Chedid', 'email': 'freddychedid@gmail.com', 'age': 20 } 
  # call the insert method to insert the data into the table 
  result = orm.insert(data) 
Updating Data
To update data in the table, you can use the update_where(condition, data, args) method. The method takes three arguments: a condition for selecting the rows to update, a dictionary of column names and new values, and a tuple of arguments to substitute into the condition. For example:

makefile
Copy code
condition = "name = %s"
data={"age": 19, "email": "madafaddoul@gmail.com"}
args=("Mada Faddoul",)
orm.update_where(condition, data, args)
Deleting Data
To delete data from the table, you can use the delete_by_id(id) method to delete a row by its ID, or the delete_where(condition, args) method to delete rows based on a condition. For example:

makefile
Copy code
condition = "name = %s"
args = ("Marylyn",)
orm.delete_where(condition, args)
or even

scss
Copy code
orm.delete_by_id(1)
Creating a Table
This method is one of the most important methods:

sql
Copy code
table_name = 'mytable' 

mytable = ORM(db_config, table_name) 
# define the columns of the new table 
columns = { 'id': 'INT NOT NULL AUTO_INCREMENT PRIMARY KEY', 
            'name': 'VARCHAR(255) NOT NULL', 
            'age': 'INT', 
            'email': 'VARCHAR(255)'} 

# create the new table using the ORM instance 
    result = mytable.create_table(columns)
    
The ORM object also provides several other methods for working with the database:
- truncate() method: Truncates the table.
- alter_table_add_column(column_name, data_type) method: Adds a new column to the table.
- drop_table() method: Drops the table.
- describe_table() method: Returns information about the table columns.
- grant_permission(user, permission) method: Grants a permission to a user for the table.
- revoke_permission(user, permission) method: Revokes a permission from a user for the table.
- join(table2, join_condition, columns=None) method: Performs a join with another table based on a join condition.
- union(): returns the union of two tables.
- order_by(): returns the rows of a table sorted by a column.
- group_by(): groups the rows of a table by one or more columns and returns the result.
- distinct(): returns the distinct values of one or more columns of a table.
- limit(): returns a limited number of rows of a table.
- create_index(): creates an index on one or more columns of a table.
- set_value(): updates the value of a column in one or more rows of a table.
- show_indexes(): returns the indexes of a table.
- replace(): replaces the row with the given ID with new data.
- insert_into_select(): inserts the result of a SELECT query into the table.

Also, you don't have to worry about inserting a wrong data type into the database. The ORM will make sure the data type you're inserting into a column respects the data type of the column, otherwise, the ORM will be printing a little message warning you to pay attention.
