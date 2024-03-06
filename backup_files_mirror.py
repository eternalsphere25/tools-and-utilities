import subprocess
from datetime import datetime

#----------------------------------------
# Define Classes
#----------------------------------------

class Robocopy:
    def __init__(self, source, destination, logfile, options):
        self.source = source
        self.destination = destination
        self.options = options
        self.logfile = logfile
        self.message_dict = {
            0: f"No files were copied. No failure was encountered. No files "
               f"were mismatched. The files already exist in the destination "
               f"directory; therefore, the copy operation was skipped.",
            1: f"All files were copied successfully.",
            2: f"There are some additional files in the destination directory "
               f"that are not present in the source directory. No files were "
               f"copied.",
            3: f"Some files were copied. Additional files were present. No "
               f"failure was encountered.",
            5: f"Some files were copied. Some files were mismatched. No "   
               f"failure was encountered.",
            6: f"Additional files and mismatched files exist. No files "
               f"were copied and no failures were encountered meaning that "
               f"the files already exist in the destination directory.",
            7: f"Files were copied, a file mismatch was present, and "
               f"additional files were present.",
            8: f"Several files did not copy."
            }

    def run_backup(self):
        backup = subprocess.run(self.robocopy_input)
        print(f"EXIT CODE: {backup.returncode}")
        print(f"OUTPUT MESSAGE: {self.message_dict[backup.returncode]}")

    def assemble_command(self):
        self.robocopy_input = [
            "robocopy",
            self.source,
            self.destination,
        ]
        self.robocopy_input.extend(self.options)
        self.robocopy_input.append(self.logfile)


#----------------------------------------
# Define Functions
#----------------------------------------

def generate_logfile_name(input_directory, input_date, input_os):
    output_string = fr"/unilog+:{input_directory}\{input_date}_{input_os}.txt"
    return output_string


#-------------------------------------------------------------------------------
# PART 0: Define variables
#-------------------------------------------------------------------------------

#Define variables
date = datetime.now().strftime("%Y%m%d_%H%M%S")
source = input("Input source directory: ") 
destination = input("Input destination directory: ")
logfile = input("Input logfile directory: ")


#-------------------------------------------------------------------------------
# PART 1: Backup Windows files with Robocopy
#-------------------------------------------------------------------------------

#Backup Windows files with Robocopy
windows_backup = Robocopy(
    source,
    destination,
    generate_logfile_name(logfile, date, "windows"),
    ["/mir", "/R:0", "/W:5", "/xo", "/v", "/tee", "/eta"]
    )
windows_backup.assemble_command()
windows_backup.run_backup()