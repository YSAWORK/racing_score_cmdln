# ./racing_reports_2018/parser_main.py
# This module handles command-line argument parsing for the racing reports application.


####### IMPORT TOOLS ######
import argparse

# create the list of input data
def choose_and_format_data(parser_results):
    """ Choose and format input data from parser results."""
    with open(f'{parser_results.files}/abbreviations.txt') as file_drivers, open(f'{parser_results.files}/start.log') as file_start, open(f'{parser_results.files}/end.log') as file_end:
        test_driver = file_drivers
        test_start = file_start
        test_end = file_end
        return test_driver, test_start, test_end, parser_results.desc, parser_results.driver

# create parser
def create_parser():
    """ Create parser for command line input."""
    parser = argparse.ArgumentParser(
        prog='Makes reports of Monaco 2018 Racing',
        usage='Print the score table of Monaco 2018 Racing of show the results of driver',
        description='Input the path to folder with files of racing`s results (abbreviation of drivers, logs with start and finish racing time.',)
    parser.add_argument('--driver', type=str, help='String for counting along characters')
    parser.add_argument('--desc', type=bool, const=True, nargs='?', help='Show the longest time racing first')
    parser.add_argument('--files', type=str, help='Path to folder with log files')
    return parser

# get formated input data from parser
def get_input_data():
    """ Get formated input data from parser."""
    return choose_and_format_data(create_parser().parse_args())