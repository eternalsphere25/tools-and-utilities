import json
import re
import sys
from pathlib import Path


###############################################################################
# STATIC DEFINITIONS
###############################################################################

###############################################################################
# CLASSES
###############################################################################

class RomanNumeral:
    # Define class variables
    dir_root = Path(__file__).resolve().parents[0]
    dir_resources = dir_root.joinpath(Path('resources'))
    file_definitions = dir_resources.joinpath(Path('definitions.json'))

    def __init__(self):
        self.load_definitions()
        self.numeral_dict = {'thousands': None,
                             'hundreds': None,
                             'tens': None,
                             'ones': None
                             }
        self.to_roman = ''

    def load_definitions(self):
        with open(__class__.file_definitions, 'r') as file_in:
            self.definitions = json.load(file_in)

    def choose_conversion_mode(self):
        while True:
            try:
                print('\n' + '='*40)
                print('Choose conversion mode:')
                print('0: Roman Numeral Quick Guide')
                print('1: Roman to Arabic')
                print('2: Arabic to Roman')
                self.mode = int(input('\nChoice: '))
                break
            except ValueError:
                print('INPUT ERROR: Non-digit character(s) entered')
                print('Please enter a number (1,2,3 etc)')

    def quick_guide(self):
        print('\n' + '-'*40)
        print('Roman Numeral Quick Guide')

        print("\nBase Roman numerals and their values:")
        for k,v in self.definitions['num_def'].items():
            print(f"{k}: {v}")

        print(f"\nNumbers are made by adding the appropriate number of "
              f"values. A few examples:")
        for k,v in self.definitions['num_def_ex'].items():
            print(f"{k}: {v}")

        print("\nBecause no numeral is allowed to repeat 4 times, "
              f"the following special abbreviations are used:")
        for k,v in self.definitions['num_abbr_def'].items():
            print(f"{k}: {v}")

        print("\nA few examples of Roman numerals including abbreviations:")
        for k,v in self.definitions['num_abbr_def_ex'].items():
            print(f"{k}: {v}")

    def remove_values(self, input_item, input_mode):
        # Set mode
        if input_mode == 'hundreds':
            check_list = ['X', 'L', 'V', 'I']
        elif input_mode == 'tens':
            check_list = ['V', 'I']

        #Remove values    
        for x in check_list:
            check = re.search(x, input_item.group(0))
            if check is not None:
                input_item = re.search(f'^.+?(?={x})', input_item.group(0))

        self.numeral_dict[input_mode] = input_item.group(0)

    def check_if_valid_roman_numeral(self, input_key, input_dict):
        if input_key in input_dict:
            return True
        else:
            return False

    def lookup_value_in_arabic(self, input_key, input_dict):
        if input_key is not None:
            if input_key in input_dict:
                value = input_dict[input_key]
        else:
            value = 0
        return value

    def roman_to_arabic(self):
        print('\n' + '-'*40)
        print("Roman to Arabic conversion mode selected")
        input_str = str(input("Enter Roman numerals to convert: "))

        #Verify all characters are vaild Roman numerals
        string_list = list(input_str)
        for x in range(len(string_list)):
            if string_list[x] not in self.definitions['num_def'].keys():
                print(f"\nERROR: Invalid character found. Valid Roman "
                      f"numerals are: {self.definitions['num_def'].keys()}")
                print("Terminating program...")
                sys.exit()

        #Verify no single character repeats 4 times in a row
        repeat = re.search(r"(.)\1{3}", input_str)
        if repeat is not None:
            print(f'\nERROR: ' + input_str + ' is not a valid Roman '
                  f'numeral (no numeral can repeat 4 times in a row)')
            print("Terminating program...")
            sys.exit()

        # Proceed with translating the number
        thousands = re.search("^M{1,3}", input_str)
        if thousands is not None:
            self.numeral_dict['thousands'] = thousands.group(0)
            new_str = input_str[len(self.numeral_dict['thousands']):]
        else:
            new_str = input_str

        hundreds = re.search("(C|D)(.)*", new_str)
        if hundreds is not None:
            if hundreds.group(0)[0] == 'C' and new_str[0] == 'X':
                new_str = new_str
            else:
                self.remove_values(hundreds, 'hundreds')
                new_str = new_str[len(self.numeral_dict['hundreds']):]
        else:
            new_str = input_str

        tens = re.search("(X|L)(.)*", input_str)
        if tens is not None:
            if tens.group(0)[0] == 'X' and new_str[0] == 'I':
                new_str = new_str
            else:
                self.remove_values(tens, 'tens')
                new_str = new_str[len(self.numeral_dict['tens']):]
        else:
            new_str = input_str

        ones = re.search("(V|I)(.)*", input_str)
        if ones is not None:
            self.numeral_dict['ones'] = ones.group(0)

        #-----------------------------------------------------------------------
        # PART 2B: Assign value to each numeral
        #-----------------------------------------------------------------------

        key_1000 = self.numeral_dict['thousands']
        key_100 = self.numeral_dict['hundreds']
        key_10 = self.numeral_dict['tens']
        key_1 = self.numeral_dict['ones']
        key_list = [key_1000, key_100, key_10, key_1]
        dict_list = [self.definitions['roman_arabic_1000_dict'],
                     self.definitions['roman_arabic_100_dict'],
                     self.definitions['roman_arabic_10_dict'],
                     self.definitions['roman_arabic_1_dict']]

        #Check if all values are valid
        for item in range(len(key_list)):
            if key_list[item] is not None:
                valid = self.check_if_valid_roman_numeral(
                    key_list[item], dict_list[item])
                if valid == False:
                    print(f"\nERROR: '{key_list[item]}' is not a valid "
                          f"Roman numeral")
                    break

        #Convert values from Roman to Arabic
        if valid is not False:
            thousands = self.lookup_value_in_arabic(
                key_1000, self.definitions['roman_arabic_1000_dict'])
            hundreds = self.lookup_value_in_arabic(
                key_100, self.definitions['roman_arabic_100_dict'])
            tens = self.lookup_value_in_arabic(
                key_10, self.definitions['roman_arabic_10_dict'])
            ones = self.lookup_value_in_arabic(
                key_1, self.definitions['roman_arabic_1_dict'])

            to_arabic = thousands + hundreds + tens + ones

            print('\nInput in Roman Numerals: ' + input_str)
            print('Output in Arabic Numerals: ' + str(to_arabic))

    def lookup_value_in_roman(self, input_value, input_dict, power):
        number = input_value * power
        if number != 0:
            value = self.get_dict_key_from_value(input_dict, number)
        else:
            value = ''
        return value

    def get_dict_key_from_value(self, input_dict, input_value):
        key_list = list(input_dict.keys())
        value_list = list(input_dict.values())
        key = key_list[value_list.index(input_value)]
        return key

    def arabic_to_roman(self):
        print('\n' + '-'*40)
        print('Arabic to Roman conversion mode selected')
        while True:
            try:
                input_string = int(input('Enter Arabic numerals to convert: '))
                break
            except ValueError:
                print('\nINPUT ERROR: Non-digit character(s) entered')
                print('Please enter a number (1,2,3 etc)\n')        

        # Working in reverse, build Roman numeral by adding each digit place
        i = 1
        for x in list(reversed([int(x) for x in str(input_string)])):
            value = self.lookup_value_in_roman(
                x, self.definitions[f'roman_arabic_{i}_dict'], i)
            self.to_roman = value + self.to_roman
            i = i*10

        print('\nInput in Arabic Numerals: ' + str(input_string))
        print('Output in Roman Numerals: ' + str(self.to_roman))


###############################################################################
# FUNCTIONS
###############################################################################

###############################################################################
# STANDALONE SCRIPT
###############################################################################

if __name__ == '__main__':
    # Generate object and choose conversion mode
    converter = RomanNumeral()
    converter.choose_conversion_mode()

    # Run program according to selection
    if converter.mode == 0:
        converter.quick_guide()
    elif converter.mode == 1:
        converter.roman_to_arabic()
    elif converter.mode == 2:
        converter.arabic_to_roman()