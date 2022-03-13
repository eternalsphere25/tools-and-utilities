#------------------------------------------------------------------------------
# This tool converts between Roman and Arabic numerals
#
# How to use: input number in either Roman or Arabic numerals when prompted
# The program is designed to throw an exception if the numeral is invalid
#
#
# Changelog
#
# Version 1.0
# 3/13/2022
# + Wrote the program
#------------------------------------------------------------------------------


import re

def check_if_valid_roman_numeral(input_key, input_dict):
    if input_key in input_dict:
        return True
    else:
        return False

def lookup_value_in_roman(input_value, input_dict, power):
    number = input_value * power
    if number != 0:
        value = get_dict_key_from_value(input_dict, number)
    else:
        value = ''
    return value

def get_dict_key_from_value(input_dict, input_value):
    key_list = list(input_dict.keys())
    value_list = list(input_dict.values())
    key = key_list[value_list.index(input_value)]
    return key

def lookup_value_in_arabic(input_key, input_dict):
    if input_key != '':
        if input_key in input_dict:
            value = input_dict[input_key]
    else:
        value = 0
    return value


#-------------------------------------------------------------------------------
# PART 0: Define global variables
#-------------------------------------------------------------------------------

roman_arabic_1000_dict = {
    'M': 1000,
    'MM': 2000,
    'MMM': 3000
    }

roman_arabic_100_dict = {
    'C': 100,
    'CC': 200,
    'CCC': 300,
    'CD': 400,
    'D': 500,
    'DC': 600,
    'DCC': 700,
    'DCCC': 800,
    'CM': 900
    }

roman_arabic_10_dict = {
    'X': 10,
    'XX': 20,
    'XXX': 30,
    'XL': 40,
    'L': 50,
    'LX': 60,
    'LXX': 70,
    'LXXX': 80,
    'XC': 90
    }

roman_arabic_1_dict = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9
    }

roman_numeral_chars = ['I','V','X','L','C','D','M']

numeral_dict = {
    'thousands': '',
    'hundreds': '',
    'tens': '',
    'ones': ''
    }

valid = True


#-------------------------------------------------------------------------------
# PART 1: Choose conversion mode
#-------------------------------------------------------------------------------

while True:
    try:
        print('\n' + '='*40)
        print('Choose conversion mode:')
        print('1: Roman to Arabic')
        print('2: Arabic to Roman')
        mode = int(input('\nChoice: '))
        break
    except ValueError:
        print('INPUT ERROR: Non-digit character(s) entered')
        print('Please enter a number (1,2,3 etc)')


#-------------------------------------------------------------------------------
# PART 2A: Divide string into base 10 units (1000, 100, 10, 1)
#-------------------------------------------------------------------------------

if mode == 1:

    print('\n' + '-'*40)
    print('Roman to Arabic conversion mode selected')
    input_string = str(input('Enter Roman numerals to convert: '))


    #Verify all characters are vaild Roman numerals
    string_list = list(input_string)
    for x in range(len(string_list)):
        if string_list[x] not in roman_numeral_chars:
            valid = False

    #Verify no single character repeats 4 times in a row
    repeat = re.search("(.)\\1{3}", input_string)


    if valid == False:
        print('\nERROR: Invalid character found. Valid Roman numerals are: ' + str(roman_numeral_chars))
    elif repeat is not None:
        print('\nERROR: ' + input_string + ' is not a valid Roman numeral (no numeral can repeat 4 times in a row)')
        valid = False
    else:
        thousands = re.search("^M{1,3}", input_string)
        if thousands is not None:
            numeral_dict['thousands'] = thousands.group(0)
        
        hundreds = re.search("(C|D)(.)*", input_string)
        if hundreds is not None:

            #Remove any tens values
            check_tens_X = re.search("X", hundreds.group(0))
            if check_tens_X is not None:
                hundreds = re.search("^.+?(?=X)", hundreds.group(0))
            check_tens_L = re.search("L", hundreds.group(0))
            if check_tens_L is not None:
                hundreds = re.search("^.+?(?=L)", hundreds.group(0))

            #Remove any ones values
            check_ones_V = re.search("V", hundreds.group(0))
            if check_ones_V is not None:
                hundreds = re.search("^.+?(?=V)", hundreds.group(0))
            check_ones_I = re.search("I", hundreds.group(0))
            if check_ones_I is not None:
                hundreds = re.search("^.+?(?=I)", hundreds.group(0))

            numeral_dict['hundreds'] = hundreds.group(0)
        
        tens = re.search("(X|L)(.)*", input_string)
        if tens is not None:

            #Remove any ones values
            check_ones_V = re.search("V", tens.group(0))
            if check_ones_V is not None:
                tens = re.search("^.+?(?=V)", tens.group(0))
            check_ones_I = re.search("I", tens.group(0))
            if check_ones_I is not None:
                tens = re.search("^.+?(?=I)", tens.group(0))

            numeral_dict['tens'] = tens.group(0)

        ones = re.search("(V|I)(.)*", input_string)
        if ones is not None:

            numeral_dict['ones'] = ones.group(0)


        #-----------------------------------------------------------------------
        # PART 2B: Assign value to each numeral
        #-----------------------------------------------------------------------

        key_1000 = numeral_dict['thousands']
        key_100 = numeral_dict['hundreds']
        key_10 = numeral_dict['tens']
        key_1 = numeral_dict['ones']

        key_list = [key_1000, key_100, key_10, key_1]
        dict_list = [roman_arabic_1000_dict, roman_arabic_100_dict, roman_arabic_10_dict, roman_arabic_1_dict]

        #Check if all values are valid
        for item in range(len(key_list)):
            if key_list[item] != '':
                valid = check_if_valid_roman_numeral(key_list[item], dict_list[item])
                if valid == False:
                    print("\nERROR: '" + key_list[item] + "' is not a valid Roman numeral")
                    break

        #Convert values from Roman to Arabic
        if valid is not False:

            thousands = lookup_value_in_arabic(key_1000, roman_arabic_1000_dict)
            hundreds = lookup_value_in_arabic(key_100, roman_arabic_100_dict)
            tens = lookup_value_in_arabic(key_10, roman_arabic_10_dict)
            ones = lookup_value_in_arabic(key_1, roman_arabic_1_dict)

            to_arabic = thousands + hundreds + tens + ones

            print('\nInput in Roman Numerals: ' + input_string)
            print('Output in Arabic Numerals: ' + str(to_arabic))


if valid == False:
    print('ERROR: Terminating program...')


#-------------------------------------------------------------------------------
# PART 3A: Divide string into base 10 units (1000, 100, 10, 1)
#-------------------------------------------------------------------------------

if mode == 2:

    print('\n' + '-'*40)
    print('Arabic to Roman conversion mode selected')

    while True:
        try:
            input_string = int(input('Enter Arabic numerals to convert: '))
            break
        except ValueError:
            print('\nINPUT ERROR: Non-digit character(s) entered')
            print('Please enter a number (1,2,3 etc)\n')        

    number = [int(x) for x in str(input_string)]

    #Assign roman numeral value to each digit place, then combine to get answer
    if len(number) == 4:
        value_1000 = lookup_value_in_roman(number[0], roman_arabic_1000_dict, 1000)
        value_100 = lookup_value_in_roman(number[1], roman_arabic_100_dict, 100)
        value_10 = lookup_value_in_roman(number[2], roman_arabic_10_dict, 10)
        value_1 = lookup_value_in_roman(number[3], roman_arabic_1_dict, 1)
        to_roman = value_1000 + value_100 + value_10 + value_1

    elif len(number) == 3:
        value_100 = lookup_value_in_roman(number[0], roman_arabic_100_dict, 100)
        value_10 = lookup_value_in_roman(number[1], roman_arabic_10_dict, 10)
        value_1 = lookup_value_in_roman(number[2], roman_arabic_1_dict, 1)
        to_roman = value_100 + value_10 + value_1

    elif len(number) == 2:
        value_10 = lookup_value_in_roman(number[0], roman_arabic_10_dict, 10)
        value_1 = lookup_value_in_roman(number[1], roman_arabic_1_dict, 1)
        to_roman = value_10 + value_1

    elif len(number) == 1:
        value_1 = lookup_value_in_roman(number[0], roman_arabic_1_dict, 1)
        to_roman = value_1
    
    print('\nInput in Arabic Numerals: ' + str(input_string))
    print('Output in Roman Numerals: ' + str(to_roman))