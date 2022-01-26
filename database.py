import sqlite3
import re


def addColumnToTable(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = getTablesInDatabase(cur)
    printAsBulletedListNoCaps(table_names)

    #Select table to work with
    table = input('\nSelect table to modify: ')

    #Get column names from table
    print('\nList of columns in database:')
    column_names = getColumnNamesFromTable(cur, table)
    print(column_names)

    while True:
        #Input new column info
        column_input = input('\nInput new column name: ')
        column_datatype = input('Input new column datatype: ').upper()
        query = "ALTER TABLE " + table + " ADD COLUMN '" + column_input + "' " + column_datatype
        cur.execute(query)
        con.commit()

        print('\nAdd another column?')
        repeat = input('Choice: ')
        if repeat == "y":
            pass
        else:
            break
    con.close()

def addValueToColumn(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = getTablesInDatabase(cur)
    printAsBulletedListNoCaps(table_names)

    #Select table to work with
    table = input('\nSelect table to modify: ')

    #Get column names from table
    print('\nList of columns in database:')
    column_names = getColumnNamesFromTable(cur, table)
    print(column_names)

    while True:
        #Select column to work with
        column = input('\nSelect column to modify: ')
        value = input('Input value: ')

        #Execute query
        query = "INSERT INTO " + table + " ('" + column + "') VALUES (" + value + ")"
        cur.execute(query)
        con.commit()

        print('\nRecord added successfully')
        print('Added record reflected below:')
        print("="*80)
        printTableContents2(cur, table)
        print("")
        print("="*80)

        #Repeat if desired
        print('\nAdd another record?')
        repeat = input('Choice (y/n): ')
        if repeat == "y":
            pass
        else:
            break
    con.close()

def createDatabase(file_path):
    con = sqlite3.connect(file_path)

def createTable(file_path):
    name_input = input('\nInput new table name: ')
    column_input = input('Input first column name (add more columns later): ')
    column_datatype = input('Input column datatype: ').upper()

    con = sqlite3.connect(file_path)
    cur = con.cursor()

    query = "CREATE TABLE IF NOT EXISTS " + name_input + "(" + column_input + " " + column_datatype + ")"
    #print(query)

    cur.execute(query)
    con.commit()
    con.close()

def getColumnNamesFromTable(cursor, input_table):
    #FYI - PRAGMA returns a tuple
    query = "PRAGMA table_info(" + input_table + ")"
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [item[1] for item in results]
    return column_names

def getDictKeyFromValue(input_dict, value):
    #FYI - Returns a list
    key = [k for k, v in input_dict.items() if v==value]
    return key

def getTablesInDatabase(cursor):
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    results = cursor.fetchall()
    table_names = [item[0] for item in results]
    return table_names

def locateDatabase():
    print('\nInput existing database (1) file path and (2) name: ')
    db_location = input('1. File Path: ')
    file_name = input('2. Name: ')
    path = str(db_location) + '\\' + str(file_name) + ('.db')
    return path 

def modifyRecord(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = getTablesInDatabase(cur)
    printAsBulletedListNoCaps(table_names)

    #Select table to work with
    table = input('\nSelect table to modify: ')

    #Get column names from table
    print('\nList of columns in database:')
    column_names = getColumnNamesFromTable(cur, table)
    print(column_names)

    #Select column to work with
    column = input('\nSelect column to modify: ')

    while True:
        #Get row number of selected month
        while True:
            month = input('\nInput month: ').title()
            if month not in row_id_month.values():
                print('ERROR: input value is not a month')
            else:
                break

        row_number = getDictKeyFromValue(row_id_month, month)[0]
        value = input('Input new value: ')

        query = "UPDATE " + table + " SET '" + column + "' = " + str(value) + " WHERE rowid = " + str(row_number) + ""

        cur.execute(query)
        con.commit()

        print('\nRecord updated successfully')
        print('Updated record reflected below:')
        print("="*80)
        printTableContents2(cur, table)
        print("")
        print("="*80)

        #Repeat if desired
        print('\nUpdate another record?')
        repeat = input('Choice (y/n): ')
        if repeat == "y":
            pass
        else:
            break

    con.close()    

def printAsBulletedListNoCaps(array):
	for x in range(len(array)):
		print('* ' + str(array[x]))

def printAsList(input_list):
	for x in range(len(input_list)):
		print(str(input_list[x]).title())

def printAsNumberedList(input_list):
	for x in range(len(input_list)):
		print(str(x) + ': ' + str(input_list[x]).title())

def printTableContents(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = getTablesInDatabase(cur)
    printAsBulletedListNoCaps(table_names)

    #Choose table to work with
    print('\nRead contents from which table?')
    table = input('Selection: ')

    #Execute query
    query = "SELECT * FROM " + table + ""
    cur.execute(query)
    results = cur.fetchall()

    #Print results
    column_names = getColumnNamesFromTable(cur, table)
    print('\nColumn Names:')
    print(column_names)
    print('\nRecords:')
    printAsList(results)

def printTableContents2(cursor, input_table):
    #Execute query
    query = "SELECT * FROM " + input_table + ""
    cursor.execute(query)
    results = cursor.fetchall()

    #Print results
    print('\nUPDATED TABLE:')
    column_names = getColumnNamesFromTable(cursor, input_table)
    print('\nColumn Names:')
    print(column_names)
    print('\nRecords:')
    printAsList(results)


#------------------------------------------------------------------------------
#STEP 0: Define global variables
#------------------------------------------------------------------------------

menu_options = [
	'1: Create New Database',
	'2: Add New Table to Database',
	'3: Add New Record to Table',
	'4: Add New Column to Table',
    '5: Modify Existing Record',
    '6: Display Table Contents'
]

row_id_month = {
    1:'January',
    2:'February',
    3:'March',
    4:'April',
    5:'May',
    6:'June',
    7:'July',
    8:'August',
    9:'September',
    10:'October',
    11:'November',
    12:'December'
}


#------------------------------------------------------------------------------
#STEP 1: Execute Program
#------------------------------------------------------------------------------

print('\nEstablishing database connection, standby...')
print('Database connection online')
print('\nSelect Option:')
printAsList(menu_options)
choice = int(input('\nChoice: '))

if choice == 1:
    name_input = input('\nInput new database name: ')
    new_database_name = str(name_input) + ('.db')
    createDatabase(new_database_name)
    print('\nDatabase successfully created!')

elif choice == 2:
    full_path = locateDatabase()
    createTable(full_path)
    print('\nTable added successfully!')

elif choice == 3:
    full_path = locateDatabase()
    addValueToColumn(full_path)
    print('\nValue(s) added successfully!')

elif choice == 4:
    full_path = locateDatabase()
    addColumnToTable(full_path)
    print('\nColumns added successfully!')

elif choice == 5:
    full_path = locateDatabase()
    modifyRecord(full_path)

elif choice == 6:
    full_path = locateDatabase()
    printTableContents(full_path)