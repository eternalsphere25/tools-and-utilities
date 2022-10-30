import re

#------------------------------------------------------------------------------
# DATABASE FUNCTIONS
#------------------------------------------------------------------------------

def get_tables_in_database(cursor):
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    results = cursor.fetchall()
    table_names = [item[0] for item in results]
    return table_names

def execute_query_prompt(input_query):
    print('\nSQL Query:\n')
    print(f'\t{input_query}')
    output_decision = input('\nExecute? y/n: ')
    return output_decision

def locate_database(db_location, db_name):
    path = f'{db_location}\\{db_name}'
    return path

def locate_database_manual():
    print('\nInput existing database (1) file path and (2) name: ')
    db_location = input('1. File Path: ')
    file_name = input('2. Database Name (do not include ".db"): ')
    path = f'{db_location}\\{file_name}.db'
    return path 


#------------------------------------------------------------------------------
# PRINT FUNCTIONS
#------------------------------------------------------------------------------

def print_as_bulleted_list_no_caps(array):
	for x in range(len(array)):
		print('* ' + str(array[x]))

def print_as_list(input_list):
	for x in range(len(input_list)):
		print(str(input_list[x]))


#------------------------------------------------------------------------------
# PRINT FUNCTIONS
#------------------------------------------------------------------------------

def regex_search(input_text, search_str):
    item_found = re.search(search_str, input_text)
    if item_found == None:
        return None
    else:
        return item_found.group(0)