#------------------------------------------------------------------------------
# This program is designed to be a Python-based CLI tool for working with 
# SQLite3 databases without needing 3rd party software.
#
# To use, execute the file in the terminal. The program will prompt you to 
# enter the database location and name.
#
#
# Changelog
#
# Version 1.1
# 10/10/2022
# + Modifications
#   - Rewrote some display code to make user input easier
#
# 9/12/2022
# + New Features
#   - Wrote the program
#------------------------------------------------------------------------------

import sqlite3
from database_config import *


#********************
#0: SHARED FUNCTIONS

def check_for_incorrect_datatype(input_list):
    error_check = []
    for x in range(len(input_list)):
        if input_list[x] not in sqlite_datatypes_list:
            error_check.append(0)
        else:
            error_check.append(1)
    return error_check

def execute_query_prompt(input_query):
    print('\nSQL Query:\n')
    print('\t' + input_query)
    output_decision = input('\nExecute? y/n: ')
    return output_decision

def get_column_names_and_datatypes_from_table(cursor, input_table):
    #FYI - PRAGMA returns a tuple 
    #PRAGMA description: https://www.sqlite.org/pragma.html#pragma_table_list
    query = "PRAGMA table_info(" + input_table + ")"
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [item[1] for item in results]
    datatypes = [item[2] for item in results]
    return column_names, datatypes

def get_tables_in_database(cursor):
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    results = cursor.fetchall()
    table_names = [item[0] for item in results]
    return table_names

def input_value_text_prompt(input_list):
    print(f"\nInput {input_list[0]} separated by a comma. Valid input examples:"
          f"\n - {input_list[1]}\n - {input_list[2]}\n - {input_list[3]}"
          f"\n - {input_list[4]}\n - {input_list[5]}")

def locate_database():
    print('\nInput existing database (1) file path and (2) name: ')
    db_location = input('1. File Path: ')
    file_name = input('2. Database Name (do not include ".db"): ')
    path = str(db_location) + '\\' + str(file_name) + ('.db')
    return path 

def print_as_bulleted_list_no_caps(array):
	for x in range(len(array)):
		print('* ' + str(array[x]))

def print_as_list(input_list):
	for x in range(len(input_list)):
		print(str(input_list[x]))

def print_two_lists_as_dict(input_list1, input_list2):
    output_dict = {input_list1[x]: input_list2[x] for x in 
                   range(len(input_list1))}
    for y in output_dict:
        print(f' - {y} [{output_dict[y]}]')

def print_table_contents_modified(cursor, input_table):
    print('\nRecord added successfully')
    print('Added record reflected below:')
    print("="*80)    
    
    #Execute query
    query = "SELECT * FROM " + input_table + ""
    cursor.execute(query)
    results = cursor.fetchall()

    #Print results
    print('\nUPDATED TABLE:')
    column_data_names = get_column_names_and_datatypes_from_table(
        cursor, input_table)
    print('\nColumn Names:')
    print(column_data_names[0])
    print(column_data_names[1])
    print('\nRecords:')
    print_as_list(results)

    print("")
    print("="*80)

def split_string_on_commas(input_string):
    split_input = input_string.split(",")
    output_list = [split_input[x].strip() for x in range(len(split_input))]
    return output_list


#********************
#1: CREATE NEW DATABASE

def create_database(file_path):
    con = sqlite3.connect(file_path)


#********************
#2: ADD NEW TABLE TO DATABASE

def aggregate_into_string_for_sql_query(input_list1, input_list2):
    output_string = ''
    for x in range(len(input_list1)):
        column_name = input_list1[x]
        datatype = input_list2[x]
        if x == len(input_list1) - 1:
            output_string += f"{column_name} {datatype}"
        else:
            output_string += f"{column_name} {datatype}, "
    return output_string

def create_table(file_path):
    proceed = False
    while proceed == False:
        # Input table name
        table_name_input = input('\nInput new table name: ')

         #Input column name(s)    
        input_value_text_prompt(input_display_text_column) 
        column_input = input('\nInput: ')
        column_input_list = split_string_on_commas(column_input)

        #Input column datatypes
        datatype_check = False
        while datatype_check == False:
            input_value_text_prompt(input_display_text_datatype)
            datatype_input = input('Input: ').upper()
            datatype_input_list = split_string_on_commas(datatype_input)

            #Check that the column and datatype inputs match
            if len(datatype_input_list) != len(column_input_list):
                print("\nERROR: Number of dataype inputs (" + 
                str(len(datatype_input_list)) + 
                ") does not match the number of column inputs (" + 
                str(len(column_input_list)) + ")!")   
            else:
                #Check for datatype errors
                error_check = check_for_incorrect_datatype(datatype_input_list)
                if all(error_check) == False:
                    print('\nERROR: Invalid datatype(s)!')      
                else:
                    #Give the green light if the above two conditions are OK:
                    datatype_check = True

        #Assemble SQL query
        aggregated_string = aggregate_into_string_for_sql_query(
            column_input_list, datatype_input_list)
        query = ("CREATE TABLE IF NOT EXISTS " + table_name_input + 
                "(" + aggregated_string + ")")

        #Confirm SQL query       
        decision = execute_query_prompt(query)
        if decision == 'y':
            proceed = True
        else:
            print('\nCancelling input...')

    #Execute query
    con = sqlite3.connect(file_path)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()


#********************
#3: ADD NEW RECORD TO TABLE

def add_value_to_column(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = get_tables_in_database(cur)
    print_as_bulleted_list_no_caps(table_names)

    #Select table to work with
    table = input('\nSelect table to modify: ')

    #Get column names from table
    print('\nList of columns and datatypes in database:')
    column_data_names = get_column_names_and_datatypes_from_table(cur, table)
    print_two_lists_as_dict(column_data_names[0], column_data_names[1])

    while True:
        proceed = False
        while proceed == False:
            #Input new values
            input_value_text_prompt(input_display_text_new_row)
            input_string = input('\nInput: ')

            #Assemble SQL query
            query = ("INSERT INTO " + table + " VALUES (" + 
                    input_string + ")")

            #Confirm SQL query       
            decision = execute_query_prompt(query)
            if decision == 'y':
                proceed = True
            else:
                print('\nCancelling input...')

        #Execute query
        cur.execute(query)
        con.commit()

        #Display modified table
        print_table_contents_modified(cur, table)

        #Repeat if desired
        print('\nAdd another record?')
        repeat = input('Choice (y/n): ')
        if repeat == "y":
            pass
        else:
            break
    con.close()


#********************
#4: ADD NEW COLUMN TO TABLE

def add_column_to_table(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = get_tables_in_database(cur)
    print_as_bulleted_list_no_caps(table_names)

    #Select table to work with
    table = input('\nSelect table to modify: ')

    #Get column names from table
    print('\nList of columns in database:')
    column_data_names = get_column_names_and_datatypes_from_table(cur, table)
    print(column_data_names[0])
    print(column_data_names[1])

    while True:
        proceed = False
        while proceed == False:
            #Input new column name info
            column_input = input('\nInput new column name: ')
                
            #Input new column datatype info
            datatype_check = False    
            while datatype_check == False:
                column_datatype = input('Input new column datatype: ').upper()
                
                #Check for datatype errors
                error_check = check_for_incorrect_datatype([column_datatype])
                if all(error_check) == False:
                    print('\nERROR: Invalid datatype(s)!')      
                else:
                    #Give the green light if the above two conditions are OK:
                    datatype_check = True

            #Assemble SQL query
            query = "ALTER TABLE " + table + " ADD COLUMN '" + column_input + "' " + column_datatype

            #Confirm SQL query       
            decision = execute_query_prompt(query)
            if decision == 'y':
                proceed = True
            else:
                print('\nCancelling input...')

        #Execute query
        cur.execute(query)
        con.commit()

        #Display modified table
        print_table_contents_modified(cur, table)

        print('\nAdd another column?')
        repeat = input('Choice (y/n): ')
        if repeat == "y":
            pass
        else:
            break

    con.close()


#********************
#5: MODIFY EXISTING RECORD

def modify_record(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = get_tables_in_database(cur)
    print_as_bulleted_list_no_caps(table_names)

    #Select table to work with
    table = input('\nSelect table to modify: ')

    while True:
        proceed = False
        while proceed == False:
            #Get column names from table
            print('\nList of columns in database:')
            column_data_names = get_column_names_and_datatypes_from_table(
                cur, table)
            print(column_data_names[0])
            print(column_data_names[1])

            #Display database data
            cur.execute("SELECT * FROM " + table)
            results = cur.fetchall()
            print_as_list(results)

            #Select column to work with
            column = input('\nSelect column to modify: ')

            #Input new value
            value = input('Input new value: ')

            #Input WHERE statement
            where = input("Input WHERE statement (don't include WHERE): ")
            query = "UPDATE " + table + " SET '" + column + "' = " + str(value) + " WHERE " + str(where)

            #Display WHERE query result
            query_where = (
                "SELECT " + column + " FROM " + table + " WHERE " + where)
            cur.execute(query_where)
            results = cur.fetchall()
            print('\nValue to be modified:')
            print_as_list(results)

            #Confirm SQL query       
            decision = execute_query_prompt(query)
            if decision == 'y':
                proceed = True
            else:
                print('\nCancelling input...')

        #Execute query
        cur.execute(query)
        con.commit()

        #Display modified table
        print_table_contents_modified(cur, table)

        #Repeat if desired
        print('\nUpdate another record?')
        repeat = input('Choice (y/n): ')
        if repeat == "y":
            pass
        else:
            break

    con.close()   


#********************
#6: DELECT RECORD FROM TABLE

def delete_record(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = get_tables_in_database(cur)
    print_as_bulleted_list_no_caps(table_names)

    #Select table to work with
    table = input('\nSelect table to modify: ')
    while True:
        proceed = False
        while proceed == False:
            #Get column names from table
            print('\nList of columns in database:')
            column_data_names = get_column_names_and_datatypes_from_table(
                cur, table)
            print(column_data_names[0])
            print(column_data_names[1])

            #Display database data
            cur.execute("SELECT * FROM " + table)
            results = cur.fetchall()
            print("")
            print_as_list(results)

            #Input WHERE statement
            where = input("\nInput WHERE statement (don't include WHERE): ")
            query = "DELETE FROM " + table + " WHERE " + where

            #Display WHERE query result
            query_where = (
                "SELECT * FROM " + table + " WHERE " + where)
            cur.execute(query_where)
            results = cur.fetchall()
            print('\nRow(s) to be dropped:')
            print_as_list(results)

            #Confirm SQL query       
            decision = execute_query_prompt(query)
            if decision == 'y':
                proceed = True
            else:
                print('\nCancelling input...')

        #Execute query
        cur.execute(query)
        con.commit()

        #Display modified table
        print_table_contents_modified(cur, table)

        #Repeat if desired
        print('\nUpdate another record?')
        repeat = input('Choice (y/n): ')
        if repeat == "y":
            pass
        else:
            break

    con.close() 


#********************
#7: DELETE TABLE FROM DATABASE

def delete_table(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = get_tables_in_database(cur)
    print_as_bulleted_list_no_caps(table_names)

    #Select table to work with
    table = input('\nSelect table to delete: ')

    #Assemble SQL query
    query = "DROP TABLE IF EXISTS " + table

    #Confirm SQL query       
    decision = execute_query_prompt(query)
    if decision == 'y':
        #Execute query
        cur.execute(query)
        con.commit()
    else:
        print('\nCancelling input...')
    con.close()


#********************
#8: RENAME TABLE

def rename_table(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = get_tables_in_database(cur)
    print_as_bulleted_list_no_caps(table_names)

    #Select table to work with
    table = input('\nSelect table to rename: ')

    #Designate new table name
    new_table_name = input('\nInput new table name: ')

    #Assemble SQL query
    query = "ALTER TABLE " + table + " RENAME TO " + new_table_name

    #Confirm SQL query       
    decision = execute_query_prompt(query)
    if decision == 'y':
        #Execute query
        cur.execute(query)
        con.commit()
    else:
        print('\nCancelling input...')
    con.close()


#********************
#9: DISPLAY TABLE CONTENTS

def print_table_contents(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    #Get tables in database
    print('\nList of tables in database:')
    table_names = get_tables_in_database(cur)
    print_as_bulleted_list_no_caps(table_names)

    #Choose table to work with
    print('\nRead contents from which table?')
    table = input('Selection: ')

    #Execute query
    query = "SELECT * FROM " + table + ""
    cur.execute(query)
    results = cur.fetchall()

    #Print results
    column_data_names = get_column_names_and_datatypes_from_table(cur, table)
    print('\nColumn Names:')
    print_two_lists_as_dict(column_data_names[0], column_data_names[1])
    print('\nRecords:')
    print_as_list(results)


#------------------------------------------------------------------------------
# DRIVER CODE
#------------------------------------------------------------------------------

def run_database_tool():
    #---------------------------------------------------------------------------
    #STEP 0: Define global variables
    #---------------------------------------------------------------------------

    menu_options = [
        '1: Create New Database',
        '2: Add New Table to Database',
        '3: Add New Record to Table',
        '4: Add New Column to Table',
        '5: Modify Existing Record',
        '6. Delete Record from Table',
        '7. Delete Table from Database',
        '8. Rename Table',
        '9: Display Table Contents'
    ]


    #---------------------------------------------------------------------------
    #STEP 1: Execute Program
    #---------------------------------------------------------------------------

    print('\nEstablishing database connection, standby...')
    print('Database connection online')
    print('\nSelect Option:')
    print_as_list(menu_options)
    choice = int(input('\nChoice: '))

    if choice == 1:
        name_input = input('\nInput new database name: ')
        new_database_name = str(name_input) + ('.db')
        create_database(new_database_name)
        print('\nDatabase successfully created!')

    elif choice == 2:
        full_path = locate_database()
        create_table(full_path)
        print('\nTable added successfully!')

    elif choice == 3:
        full_path = locate_database()
        add_value_to_column(full_path)
        print('\nRows(s) added successfully!')

    elif choice == 4:
        full_path = locate_database()
        add_column_to_table(full_path)
        print('\nColumn(s) added successfully!')

    elif choice == 5:
        full_path = locate_database()
        modify_record(full_path)

    elif choice == 6:
        full_path = locate_database()
        delete_record(full_path)

    elif choice == 7:
        full_path = locate_database()
        delete_table(full_path)

    elif choice == 8:
        full_path = locate_database()
        rename_table(full_path)

    elif choice == 9:
        full_path = locate_database()
        print_table_contents(full_path)


#------------------------------------------------------------------------------
# UNCOMMENT BELOW TO RUN CODE DIRECTLY
#------------------------------------------------------------------------------

run_database_tool()