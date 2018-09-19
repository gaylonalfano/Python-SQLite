'''
Let's say we want to create an app that allows us to add, update
and delete employees from a database, as well as able to grab
employee info from that databases.

SQLite Documentation:  https://www.sqlite.org/docs.html

'''
import sqlite3
from employee import Employee  # can import module since it's in same directory

# Need a connection object that represents our DB.
# It'll either create the file and/or connect to the DB. .db looks like gibberish
'''
SUPER HANDY. You can connect to a database stored in memory:

conn = sqlite3.connect(':memory:')

This gives us a DB that lives in RAM and that's useful for testing if you want a 
fresh clean database for EVERY RUN. So, basically it's kinda like "w" write mode
where it'll completely overwrite what was previously there. The benefit of all
this is that you don't have to COMMENT EVERYTHING OUT. It won't insert multiple
values or get errors when trying to create tables that already exist, etc.

This is nice when you're doing your testing. And when you're ready you can just 
pass in a file and your database will be stored like we did earlier (employee.db)

'''
#conn = sqlite3.connect('employee.db')  
conn = sqlite3.connect(':memory:')

# Let's create a cursor so we can execute SQL commands using execute method
c = conn.cursor()

# SQLite Datatypes available:(NULL, INTEGER, REAL (float), TEXT, BLOB)
# Use """ """ for multi-line SQL and single pair for one line.
c.execute("""CREATE TABLE employees (
            first text,
            last text,
            pay integer
            )""")

''' 
Let's prototype a basic application where we use our created table to 
insert/add employees, get employee info by name, update pay, delete employee, etc.
This is a more PYTHONIC way of doing thing. 

TRICK/TIP CONTEXT MANAGERS: 
It's a pain to commit() after every time you insert, update, or delete. If you know
about CONTEXT MANAGERS using the WITH statment, then we're in luck. CONTEXT MANAGERS
allow us to configure a SETUP and TEARDOWN of resources automatically. In SQLite, 
connection objects can be used as context managers that automatically commit or 
roll back transactions. So transactions will auto commit unless there's an exceptions,
in which case it will be automatically rolled back.

*NOTE* use WITH statments for INSERT, UPDATE, DELETE since these have to be committed.

with conn:
    c.execute(...)

After you create all your functions for the application, you can basically delete/remove
all of the previous code (except conn.close()).
'''
def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
                {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchall()


def update_pay(emp, pay):
    with conn:
        c.execute("UPDATE employees SET pay=:pay WHERE last=:last AND first=:first",
                {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(emp):
    with conn:
        c.execute("DELETE FROM employees WHERE first=:first AND last=:last", 
                {'first': emp.first, 'last': emp.last})



emp_1 = Employee('John', 'Doe', 80000)  # These are just Python objs but
emp_2 = Employee('Jane', 'Doe', 90000)  # haven't been inserted into DB yet

insert_emp(emp_1)
insert_emp(emp_2)

emps = get_emps_by_name('Doe')
print(emps)  # [('John', 'Doe', 80000), ('Jane', 'Doe', 90000)]

update_pay(emp_2, 95000)
remove_emp(emp_1)

emps = get_emps_by_name('Doe')
print(emps)

conn.close()



 # ================ BELOW was done before adding ABOVE functions ===========
 # === Can add, delete, update, etc. now by just using the new functions ===

'''
After you create some Python Class objects (emp_1, emp), they still haven't
been added to the DB yet. You might be tempted to use string formatting but 
this is BAD PRACTICE when using DBs in Python. Example:

"... VALUES ('{}', '{}', {})".format(emp_1.first, emp_1.last, emp_1.pay)

If you're accepting values from an enduser (website, etc.) then this is vulnerable
to SQL injection attacks. Basically, there are values that I could set these 
variables to equal to that could break the entire database. The reason for that 
is that they are not properly escaped.

There are two different ways to do this: 
1. Use "?" instead of {} and add your values to the second argument of the execute() method. 
Note that the second argument MUST be in a TUPLE regardless if it's just one value. 
In the case that it's just a single value, to make a TUPLE you add a ',' ('Schafer',).
The ? is a DB API placeholder and you don't need quotes anymore.

c.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))

2. COREY'S PREFERRED METHOD. Instead of ?, we use :column. We still pass a second argument
to execute() but this time it's a DICT.

c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", 
    {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay})

'''
# Now that we have the table, let's comment it out and start adding data
#c.execute("INSERT INTO employees VALUES ('Mary', 'Schafer', 70000)")

# Added "Mary" so this is just being explicit to commit() again before query
#conn.commit() 

# c.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))

# conn.commit()

# c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", 
#     {'first': emp_2.first, 'last': emp_2last, 'pay': emp_2.pay})

# conn.commit()

'''
At first we've been typing in the values directly into SELECT statements.
However, the way you'll mostly use this with Python is that you'll have 
some variables in your code that you will insert into your SQL query.

Example - Let's start using the Employee Class
def __init__(self, first, last, pay)

After importing the module: from employee import Employee
We can add some code using that class up above our INSERT statement.

'''
# Let's query the DB to see if Corey was added (see above for how to use Python)
#c.execute("SELECT * FROM employees WHERE last='Schafer'")

# Using ? placeholder and tuple
# c.execute("SELECT * FROM employees WHERE last=?", ('Schafer',))  # Note the comma!

# print(c.fetchall())

# # Using :column placeholder and dictionary
# c.execute("SELECT * FROM employees WHERE last=:last", {'last': 'Doe'})

# print(c.fetchall())
# Note that the SELECT statement is going to provide results we can iterate through.
#print(c.fetchone()) # It will get the next row in results or None. Sort of like next()
#c.fetchmany(5)  # Returns a LIST of n rows.
#print(c.fetchall())  # Returns a LIST of remaining rows or empty list.


# Let's do a couple more things before running this (create table code)
# commit() - commits the current transaction. If you're not seeing anyting in the DB,
# then good chance you haven't committed.
# conn.commit()

# It's also good practice to close your DB connection using conn.close()
# conn.close()

# After you run it, it's good. If you try to run again you get this error:
# sqlite3.OperationalError: table employees already exists

















# import sqlite3
# from employee import Employee

# conn = sqlite3.connect(':memory:')

# c = conn.cursor()

# c.execute("""CREATE TABLE employees (
#             first text,
#             last text,
#             pay integer
#             )""")


# def insert_emp(emp):
#     with conn:
#         c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


# def get_emps_by_name(lastname):
#     c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
#     return c.fetchall()


# def update_pay(emp, pay):
#     with conn:
#         c.execute("""UPDATE employees SET pay = :pay
#                     WHERE first = :first AND last = :last""",
#                   {'first': emp.first, 'last': emp.last, 'pay': pay})


# def remove_emp(emp):
#     with conn:
#         c.execute("DELETE from employees WHERE first = :first AND last = :last",
#                   {'first': emp.first, 'last': emp.last})

# emp_1 = Employee('John', 'Doe', 80000)
# emp = Employee('Jane', 'Doe', 90000)

# insert_emp(emp_1)
# insert_emp(emp)

# emps = get_emps_by_name('Doe')
# print(emps)

# update_pay(emp, 95000)
# remove_emp(emp_1)

# emps = get_emps_by_name('Doe')
# print(emps)

# conn.close()