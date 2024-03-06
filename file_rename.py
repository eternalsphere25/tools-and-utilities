from pathlib import Path


def clean_input_path_str(input_str):
	if (input_str.startswith('"') == True and input_str.endswith('"') == True):
		output_str = Path(input_dir_str[1:-1])
	else:
		output_str = Path(input_dir_str)
	return output_str


#------------------------------------------------------------------------------
# STEP 1: Search for files to rename
#------------------------------------------------------------------------------

print('\nEstablishing connection, standby...')
print('Connection online')

# Get user input
file_ext = str(input(
	'\nSet file extension to search for (do not include dot): '))
input_dir_str = str(input('Input folder path: '))

# Clean up input string
input_dir = clean_input_path_str(input_dir_str)

# Find all files of specified type
file_list = sorted(input_dir.glob(f"*.{file_ext}"))

# Display files found that match input file extension
print('\nList of data files found: ')
print(*[f"- {item.name}" for item in file_list], sep="\n")


#------------------------------------------------------------------------------
# STEP 2: Remove/Replace selected characters from file name
#------------------------------------------------------------------------------

# Show options menu and get user choice
print('\nSelect task:')
print('1. Remove characters')
print('2. Replace characters')
choice = int(input('Selection: '))

# Perform selected operation
print('\nRenaming files...')
if choice == 1:
	# Select portion to remove
	remove_this = str(input('\nInput characters to remove: '))

	# Rename files
	for input_file in file_list:
		print(f"File {file_list.index(input_file)+1} of {len(file_list)}")
		input_file.replace(input_file.with_name(
			input_file.name.replace(remove_this, "")))
		print("File processed")

elif choice == 2:
	# Select portion to rename
	replace_this = str(input('\nInput characters to replace: '))
	with_this = str(input('Input replacement characters: '))

	# Rename files
	for input_file in file_list:
		print(f"File {file_list.index(input_file)+1} of {len(file_list)}")
		
		input_file.replace(input_file.with_name(
			input_file.name.replace(replace_this, with_this)))
		print('File processed')

else:
	print('ERROR: Invalid input')

# Display new names
file_list = sorted(input_dir.glob(f"*.{file_ext}"))
print('\nList of new file names: ')
print(*[f"- {item.name}" for item in file_list], sep="\n")


#------------------------------------------------------------------------------
# STEP 3: Close program
#------------------------------------------------------------------------------

# End program
print('\nProcess completed')
print('Connection terminated')