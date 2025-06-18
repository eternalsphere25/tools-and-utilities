#------------------------------------------------------------------------------
# This program takes an input folder with image files, then automatically sorts
# and copies them over to the server
#------------------------------------------------------------------------------

import subprocess
import sys
import tomllib
from datetime import datetime, timedelta
from pathlib import Path


###############################################################################
# STATIC DEFINITIONS
###############################################################################

###############################################################################
# CLASSES
###############################################################################

class Transfer:
    # Define class variables
    dir_root = Path(__file__).resolve().parents[0]
    file_types = ['nef', 'jpg', 'mp4']

    def __init__(self, input_dir):
        self.dir_source = input_dir
        self.import_config()
        self.dir_dest = Path(self.config['destination']['destination'])

    def import_config(self):
        config_file = __class__.dir_root.joinpath(Path('config.toml'))
        with open(config_file, 'rb') as file_in:
            self.config = tomllib.load(file_in)

    def get_file_list(self, input_dir, input_ext):
        glob_result = input_dir.glob(f'*.{input_ext}')
        output_list = [x for x in glob_result if x.is_file()]
        return output_list

    def build_file_list(self):
        # Generate file lists
        print("\nSearching for photo and video files...")
        for x in __class__.file_types:
            setattr(self, f'files_{x}', self.get_file_list(self.dir_source, x))
            print(f"- {len(getattr(self, f'files_{x}'))} {x.upper()} "
                  f"file(s) found")

    def confirm_transfer(self):
        do_transfer = input(f"\nProceed with file transfer? y/n\nChoice: ")
        if do_transfer.casefold() == "y":
            pass
        else:
            print('Transfer cancelled...')
            sys.exit()

    def get_file_mod_dates(self, input_list):
        list_of_dates, files_with_dates = [], {}
        for item in input_list:
            file_timestamp = item.stat().st_mtime
            file_datetime = datetime.fromtimestamp(file_timestamp)
            files_with_dates[item] = file_datetime.date()
            if file_datetime.date() not in list_of_dates:
                list_of_dates.append(file_datetime.date())
        return list_of_dates, files_with_dates

    def run_transfer(self):
        for x in __class__.file_types:
            file_list = getattr(self, f'files_{x}')
            if len(file_list) > 0:
                # First get a list of all dates associated with the files
                list_dates, files_with_dates = self.get_file_mod_dates(
                    file_list)
                for date in list_dates:
                    # Assemble a destination path; make one if it doesn't exist
                    if x == 'jpg':
                        dest_path = self.dir_dest.joinpath(
                            f'[{str(date.year)}]', str(date))
                    else:
                        dest_path = self.dir_dest.joinpath(
                            f'[{str(date.year)}]', str(date), "Raws")
                    if dest_path.exists() == False:
                        dest_path.mkdir(parents=True)
                        print(f"[NOTICE] New directory '{dest_path}' made")
                    
                    # Check if the files exist before running robocopy
                    existing_files = self.get_file_list(dest_path, x)
                    if len(existing_files) > 0:
                        print(f"[NOTICE] {x.upper()} files already exist in "
                              f"destination: '{dest_path}'")
                        print(f"[NOTICE] No files transferred")
                    else:
                        self.run_robocopy(date, dest_path)

    def run_robocopy(self, input_date, input_path):
        # Set flags to use with robocopy
        date_1 = str(input_date).replace("-","")
        date_2 = str(input_date + timedelta(days=1)).replace("-","")
        date_now = str(datetime.now().date()).replace("-","")
        time_now = str(datetime.now().time()).replace(":","").split(".")[0]
        log_file = self.dir_dest.joinpath(Path(\
            'Robocopy Transfer Logs', f'{date_now + '_' + time_now}.txt'))

        # Copy files from source to destination with robocopy
        subprocess.run(['robocopy', f'{str(self.dir_source)}', 
                        f'{str(input_path)}', '/s', '/xo', '/v', 
                        f'/maxage:{date_1}', f'/minage:{date_2}', 
                        f'/unilog+:{log_file}', '/mt:128', '/tee', '/eta'])


###############################################################################
# FUNCTIONS
###############################################################################

###############################################################################
# STANDALONE SCRIPT
###############################################################################

if __name__ == '__main__':
    # Set a directory as the source of the files
    dir_source = Path(input(f"\nInput source directory: ").replace('"', ''))
    if Path.exists(dir_source) == False:
        print(f'[ERROR] The specified directory "{dir_source}" does not exist')
        print("Program terminating...")
        sys.exit()
    
    # Generate object
    transfer = Transfer(dir_source)

    # Build list of files inside the directory
    transfer.build_file_list()

    # Confirm before proceeding with transfer
    transfer.confirm_transfer()

    # Transfer files
    transfer.run_transfer()