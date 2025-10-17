# ./racing_reports_2018/main.py
# This module processes racing data and generates reports.

###### IMPORT TOOLS ######
import  datetime
from functools import lru_cache
from dataclasses import dataclass
import PyPDF2
import io

# This module processes racing results and provides PDF text extraction functionality

# class with racing info
@dataclass
class Drivers:
      """ Class with racing info about drivers."""
      name: str
      abbr: str
      team: str
      start_time: datetime
      end_time: datetime
      time: datetime.timedelta=None
      error: str=None

# get text from pdf file
def get_text_from_pdf(pdf_path) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content from the PDF
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: If there's an error reading the PDF
    """
    try:
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Initialize text variable
            text = ""
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
                
            return text.strip()
            
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    except Exception as e:
        raise Exception(f"Error reading PDF file {pdf_path}: {str(e)}")

# get text from pdf file using file-like object
def get_text_from_pdf_file_object(pdf_file) -> str:
    """
    Extract text content from a PDF file-like object.
    
    Args:
        pdf_file: File-like object containing PDF data
        
    Returns:
        str: Extracted text content from the PDF
        
    Raises:
        Exception: If there's an error reading the PDF
    """
    try:
        # Create a PDF reader object from file-like object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Initialize text variable
        text = ""
        
        # Extract text from each page
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
            
        return text.strip()
        
    except Exception as e:
        raise Exception(f"Error reading PDF file object: {str(e)}")

# get info about time of start/finish from files
def get_datetime_info(file) -> dict: # dict('driver abbreviation' : driver time os start/finish in datetime format, ...)
    """ Get datetime info from file and return as dictionary."""
    with open(f'{file.name}') as time_data:
        datetime_dict = {}
        for item in enumerate(time_data.read().splitlines()):
            if item[1] in ('', ' ', '_', None):
                continue
            elif not item[1][:3].isalpha() or len(item[1][3:]) != 23:
                print(f'{item[1]} not included in results -- wrong data format in line {item[0] + 1} ({file.name}).')
            else:
                datetime_dict[item[1][:3]] = datetime.datetime.fromisoformat(item[1][3:].replace('_', 'T').strip())
        return datetime_dict

# get info about drivers from file
def get_drivers_info(abbr_file, start_datetime, end_datetime) -> list:
    """ Get info about drivers from file and return as list of class(Drivers) objects."""
    with open(f'{abbr_file.name}') as driver_abbrv:
        drivers_list = list()
        for item in enumerate(driver_abbrv.read().splitlines()):
            if item[1] in ('', ' ', '_', None):
                continue
            elif len(item[1].split('_')) != 3:
                print(f'{item[1]} not included in results -- wrong data format in line {item[0] + 1} ({abbr_file.name})')
            else:
                driver_data = item[1].split('_')
                try:
                    driver = Drivers(
                        abbr=driver_data[0],
                        name=driver_data[1],
                        team=driver_data[2],
                        start_time=start_datetime[driver_data[0]],
                        end_time=end_datetime[driver_data[0]], )
                    driver.time = driver.end_time - driver.start_time
                    if int(driver.time.total_seconds()) < 0:
                        driver.error = 'incorrect data'
                    drivers_list.append(driver)
                except KeyError:
                    print(f'{driver.name} ({driver.abbr}) hasn`t enough data. Not included in results')
        return drivers_list

# built report
@lru_cache(maxsize=100)
def built_report(abbr, start_data, end_data, range_rule) -> list: # list of class(Drivers) objects, sorted by the time of racing
    """ Built report based on input data and return sorted list of class(Drivers) objects."""
    start_dict = get_datetime_info(start_data)
    end_dict = get_datetime_info(end_data)
    drivers_info = get_drivers_info(abbr, start_dict, end_dict)
    result = list(sorted(drivers_info, key=lambda x: x.time))
    if range_rule:
        result = reversed(result)
    return result

# print report
@lru_cache(maxsize=100)
def print_report(data_drivers, data_start, data_end, range_type, driver_name):
    """ Print report based on input data. If driver_name is specified, print only info about this driver."""
    results = built_report(data_drivers, data_start, data_end, range_type)
    if driver_name:
        driver = list(filter(lambda el: el.name == driver_name, results))
        print(f'Results of racing {driver[0].name} from {driver[0].team}:\n\t'
              f'- Start of lap: {driver[0].start_time}\n\t'
              f'- End of lap:   {driver[0].end_time}\n\t'
              f'- Time of lap:  {driver[0].time}')
    else:
        print('------------------------------------Report of Monaco 2018 Racing-----------------------------------------\n'
              '# |       Driver          |            Team              |             Time            |       Errors \n'
              '---------------------------------------------------------------------------------------------------------')
        for result in enumerate(results):
            print('%-3s %-20s  |   %-25s  |  %-25s  |  %s' % (result[0] + 1, result[1].name, result[1].team, result[1].time, result[1].error))
            if result[0] + 1 == 15:
                print('\n----------------------------------------ELIMINATED-------------------------------------------------------\n')

if __name__ == '__main__': # pragma: no cover
    import sys
    sys.path.append("racing_reports_2018")
    from parser_main import get_input_data
    print_report(*get_input_data())
