#-------------------------------------------------------------------------------
# This libracy contains functions to calculate outliers from an input sequence 
# of numbers based on both the interquartile range (IQR) and the z-score methods
#
# IQR method explained:
# https://online.stat.psu.edu/stat200/lesson/3/3.2
#
# Z-Score method explained:
# https://www.statisticshowto.com/probability-and-statistics/z-score/
#
#
# Changelog
#
# Version 1.0
# 10/10/2022
# + New Features:
#   - Wrote the functions
#-------------------------------------------------------------------------------

import numpy as np

def calc_outliers_IQR(input_data_list):
    #Calculate 25th and 75th percentiles
    percentile_25 = np.percentile(input_data_list, 25)
    percentile_75 = np.percentile(input_data_list, 75)
    iqr = percentile_75 - percentile_25

    #Calculate max and min values
    upper_bound = percentile_75 + (1.5*iqr)
    lower_bound = percentile_25 - (1.5*iqr)

    #Calculate outliers (IQR)
    output_dict = {}
    for i in range(len(input_data_list)):
        current_item = input_data_list[i]
        if current_item < upper_bound:
            if current_item > lower_bound:
                pass
            else:
                output_dict[i] = current_item
        else:
            output_dict[i] = current_item
    return output_dict

def find_outliers(input_df, var_list, condition):
    #print(f'\n\nOutlier detection results for {condition}')
    for item in range(len(var_list)):
        current_variable = var_list[item]
        data = input_df[current_variable].to_dict()
        values = list(data.values())
        outliers = calc_outliers_IQR(values)
        #print(f"\nOutliers for '{current_variable}':")
        #print(outliers)

        #Calculate mean, median, and stdev for z-score
        mean_val = sum(values) / len(values)
        median_val = np.median(values)
        stdev_val = np.std(values)
        #print(f'Mean: {mean_val}')
        #print(f'Median: {median_val}')
        #print(f'Standard Deviation: {stdev_val}')

def generate_winsorized_list(input_list, pct5, pct95):
    output_list = []
    for x in range(len(input_list)):
        current_value = input_list[x]
        if current_value < pct5:
            output_list.append(pct5)
        elif current_value > pct95:
            output_list.append(pct95)
        else:
            output_list.append(current_value)
    return output_list

def process_outliers(input_df, var_list, condition):
    for item in range(len(var_list)):
        current_variable = var_list[item]
        data = input_df[current_variable].to_dict()
        values = list(data.values())

        #Calculate 5th and 95th percentiles
        percentile_5 = np.percentile(values, 5)
        percentile_95 = np.percentile(values, 95)
        
        #Replace extreme values
        winsorized_list = generate_winsorized_list(
            values, percentile_5, percentile_95)
        input_df[var_list[item]] = winsorized_list
    #print('\nOutliers for condition ' + condition + ' processed')
