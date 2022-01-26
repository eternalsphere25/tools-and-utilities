import os
import glob

def listRange(index, input):
	value = list(range(index,len(input)))
	return value

def printAsList(input, index):
	print(input[index])


#------------------------------------------------------------------------------
#STEP 1: Search for files to rename
#------------------------------------------------------------------------------

print('\nEstablishing connection, standby...')
print('Connection online')

#Find all files of specified type
file_extension = str(input(
	'\nSet file extension to search for (do not include dot): '))
directory = str(input('Input folder path: '))
files = glob.glob(directory + '/*' + file_extension)
files_list_length = listRange(1, files)

#Extract file names from full file address
files_name_only = [os.path.basename(files[0])]
for f in files_list_length:
	files_name_only.append(os.path.basename(files[f]))
	pass

#List out all data files found in folder
print('\nList of data files found: ')
files_list_length = listRange(0, files)
for names in files_list_length:
	printAsList(files_name_only, names)

print('\nSelect task:')
print('1. Remove characters')
print('2. Replace characters')
choice = int(input('Selection: '))

if choice == 1:
	#---------------------------------------------------------------------------
	#STEP 2a: Remove selected characters from file name
	#---------------------------------------------------------------------------

	#Select portion to remove
	remove_this = str(input('\nInput characters to remove: '))

	#Rename files
	print('\nRenaming files...')
	file_dir = directory + "\\"
	for file in os.listdir(directory):
		print('\nFile ' + str(files_name_only.index(file)+1) + ' of ' + str(
			len(files_list_length)))
		os.replace(file_dir + file, file_dir + file.replace(remove_this, ''))
		print('File renamed')

	#Display new names
	files = glob.glob(directory + '/*' + file_extension)
	files_list_length = listRange(1, files)

	#Extract file names from full file address
	files_name_only = [os.path.basename(files[0])]
	for f in files_list_length:
		files_name_only.append(os.path.basename(files[f]))
		pass

	#List out all data files found in folder
	print('\nList of new file names: ')
	files_list_length = listRange(0, files)
	for names in files_list_length:
		printAsList(files_name_only, names)

elif choice == 2:
	#---------------------------------------------------------------------------
	#STEP 2b: Replace selected characters in file name
	#---------------------------------------------------------------------------

	#Select portion to remove
	replace_this = str(input('\nInput characters to replace: '))
	with_this = str(input('Input replacement characters: '))

	#Rename files
	print('\nRenaming files...')
	file_dir = directory + "\\"
	for file in os.listdir(directory):
		print('\nFile ' + str(files_name_only.index(file)+1) + ' of ' + str(
			len(files_list_length)))
		os.replace(file_dir + file, file_dir + file.replace(
			replace_this, with_this))
		print('File renamed')

	#Display new names
	files = glob.glob(directory + '/*' + file_extension)
	files_list_length = listRange(1, files)

	#Extract file names from full file address
	files_name_only = [os.path.basename(files[0])]
	for f in files_list_length:
		files_name_only.append(os.path.basename(files[f]))
		pass

	#List out all data files found in folder
	print('\nList of new file names: ')
	files_list_length = listRange(0, files)
	for names in files_list_length:
		printAsList(files_name_only, names)

else:
	print('ERROR: Invalid input')


#------------------------------------------------------------------------------
#STEP 3: Close program
#------------------------------------------------------------------------------

#End program
print('\nProcess completed')
print('Connection terminated')