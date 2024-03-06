#------------------------------------------------------------------------------
# This program takes an input folder with image files, then automatically sorts
# and copies them over to the server
#------------------------------------------------------------------------------

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_file_list(input_ext):
    glob_result = dir_source.glob(f'*.{input_ext}')
    dirs = [x for x in glob_result if x.is_dir]
    return dirs

def get_file_mod_dates(input_list):
    list_of_dates = []
    files_with_dates = {}
    for item in input_list:
        file_timestamp = item.stat().st_mtime
        file_datetime = datetime.fromtimestamp(file_timestamp)
        files_with_dates[item] = file_datetime.date()
        if file_datetime.date() not in list_of_dates:
            list_of_dates.append(file_datetime.date())

    return list_of_dates, files_with_dates

def make_path_if_none(input_path):
    if input_path.exists() == False:
        input_path.mkdir(parents=True)
        print(f'[NOTICE] New directory "{input_path}" made')

def run_robocopy(input_date):
    # Set flags to use with robocopy
    date_1 = str(input_date).replace("-","")
    date_2 = str(input_date + timedelta(days=1)).replace("-","")
    date_now = str(datetime.now().date()).replace("-","")
    time_now = str(datetime.now().time()).replace(":","").split(".")[0]
    log_file = (f"D:\写真\Robocopy Transfer Logs"
                f"\{date_now + '_' + time_now}.txt")

    # Copy files from source to destination with robocopy
    subprocess.run(["robocopy", f"{str(dir_source)}", f"{str(dest_path)}", 
                    "/s", "/xo", "/v", f"/maxage:{date_1}",
                    f"/minage:{date_2}", f"/unilog+:{log_file}", 
                    "/mt:128", "/tee", "/eta"])


#------------------------------------------------------------------------------
# PART 0: Define global constants
#------------------------------------------------------------------------------

# Set filename and absolute file path
filename = Path(__file__).name
cwd = Path(__file__).parent

# Set destination root directory
root_dir_dest = Path("D:/写真/")

# Set media file types to search for
file_types = {"nef", "jpg", "mp4"}


#------------------------------------------------------------------------------
# PART 1: Import data
#------------------------------------------------------------------------------

# Set a directory as the source of the files
dir_source = Path(input(f"Input source directory:"))
if Path.exists(dir_source) == False:
    print(f'[ERROR] The specified directory "{dir_source}" does not exist')
    print("Program terminating...")
    sys.exit()


#------------------------------------------------------------------------------
# PART 2: Find files
#------------------------------------------------------------------------------

# Build a list of files inside the directory
files_nef, files_jpg, files_mp4 = [], [], []
for file_type in file_types:
    if file_type == "nef":
        files_nef = get_file_list(file_type)
        print(f"{len(files_nef)} NEF file(s) found")
    elif file_type == "jpg":
        files_jpg = get_file_list(file_type)
        print(f"{len(files_jpg)} JPG file(s) found")
    elif file_type == "mp4":
        files_mp4 = get_file_list(file_type)
        print(f"{len(files_mp4)} MP4 file(s) found")


#------------------------------------------------------------------------------
# PART 3: Transfer files to appropriate destinations
#------------------------------------------------------------------------------

# NEF Files
if len(files_nef) > 0:
    # First get a list of all dates associated with the files
    list_dates_nef, files_with_dates_nef = get_file_mod_dates(files_nef)
    for date in list_dates_nef:
        # Assemble a destination path; make one if it doesn't exist
        dest_path = Path(root_dir_dest, f"[{str(date.year)}]", 
                         f"{str(date)}", "Raws")
        make_path_if_none(dest_path)

        # Check if the files exist before running robocopy
        existing_files = get_file_list(".nef")
        if len(existing_files) > 0:
            run_robocopy(date)
        else:
            print(f'[NOTICE] NEF files already exist in source destination: '
                  f'"{dest_path}"')
            print(f"[NOTICE] No files transferred")

# JPG Files
if len(files_jpg) > 0:
    # First get a list of all dates associated with the files
    list_dates_jpg, files_with_dates_jpg = get_file_mod_dates(files_jpg)
    for date in list_dates_jpg:
        # Assemble a destination path; make one if it doesn't exist
        dest_path = Path(root_dir_dest, f"[{str(date.year)}]", f"{str(date)}")
        make_path_if_none(dest_path)

        # Check if the files exist before running robocopy
        existing_files = get_file_list(".jpg")
        if len(existing_files) > 0:
            run_robocopy(date)
        else:
            print(f'[NOTICE] JPG files already exist in source destination: '
                  f'"{dest_path}"')
            print(f"[NOTICE] No files transferred")

# MP4 Files
if len(files_mp4) > 0:
    # First get a list of all dates associated with the files
    list_dates_mp4, files_with_dates_mp4 = get_file_mod_dates(files_mp4)
    for date in list_dates_mp4:
        # Assemble a destination path; make one if it doesn't exist
        dest_path = Path(root_dir_dest, f"[{str(date.year)}]", 
                         f"{str(date)}", "Raws")
        make_path_if_none(dest_path)

        # Check if the files exist before running robocopy
        existing_files = get_file_list(".mp4")
        if len(existing_files) > 0:
            run_robocopy(date)
        else:
            print(f'[NOTICE] MP4 files already exist in source destination: '
                  f'"{dest_path}"')
            print(f"[NOTICE] No files transferred")